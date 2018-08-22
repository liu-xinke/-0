'''
利用蒙特卡洛树搜索算法实现类似alphazero自我博弈
蒙特卡洛树搜索四步骤:
选择 --> 拓展 --> 模拟 --> 回溯
参考资料:https://github.com/junxiaosong/AlphaZero_Gomoku
        https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
        https://en.wikipedia.org/wiki/AlphaZero
'''

import numpy as np
import copy

def softmax(x):
    probs = np.exp(x - np.max(x)) #  np.exp(a) 对矩阵a中每个元素取指数函数
    probs /= np.sum(probs)         

class TreeNode():
    '''
    该类模仿蒙特卡洛树中的各个节点,
    每个节点都会拥有自己的Q值,获胜概率P及被访问前的得分u
    '''
    def __init__(self, parent, prior_p):
        self._parent = parent
        self._children = {}  # 存储节点行为
        self._n_visits = 0   # 初始化访问次数
        self._Q = 0          # 初始化Q值
        self._u = 0          # 初始化得分
        self._P = prior_p

    def expand(self, action_priors):
        """
        向下拓展新的子节点
        """
        for action, prob in action_priors:
            if action not in self._children:
                self._children[action] = TreeNode(self, prob)

    def select(self, c_puct):
        """
        选择得分最高的子节点进行下一步操作
        """
        return max(self._children.items(),
                   key=lambda act_node: act_node[1].get_value(c_puct))

    def update(self, leaf_value):
        """
        通过对该子节点下的叶节点情况判断来更新子节点Q值        
        """
        # 更新访问次数.
        self._n_visits += 1
        # 对所有的叶节点访问后取平均值作为该子节点的Q值
        self._Q += 1.0*(leaf_value - self._Q) / self._n_visits

    def update_recursive(self, leaf_value):
        """
        递归函数
        用于二级节点及之后的节点,更新节点的值
        """
        if self._parent:
            self._parent.update_recursive(-leaf_value)
        self.update(leaf_value)

    def get_value(self, c_puct):
        """
        计算并返回这个节点的值.
        通过Q值和访问次数 利用公式计算出该节点的得分
        """
        self._u = (c_puct * self._P * np.sqrt(self._parent._n_visits) / (1 + self._n_visits))
        return self._Q + self._u

    def is_leaf(self):
        """
        判断是否为叶节点
        """
        return self._children == {}

    def is_root(self):
        """
        判断是否为根节点
        """
        return self._parent is None

class MCTS():
    """蒙特卡洛树搜索函数"""

    def __init__(self, policy_value_fn, c_puct=5, n_playout=10000):
        """
        policy_value_fn: 获取当前棋盘情况,然后将通过计算得到一个(动作,概率)元组,最后返回一个在[-1,1]之间的得分值
        c_puct: 通过给定的值来决定计算的深度 值越高深度越大,函数收敛速度越慢.
        """
        self._root = TreeNode(None, 1.0)
        self._policy = policy_value_fn
        self._c_puct = c_puct
        self._n_playout = n_playout

    def _playout(self, state):
        """Run a single playout from the root to the leaf, getting a value at
        the leaf and propagating it back through its parents.
        State is modified in-place, so a copy must be provided.
        """
        node = self._root
        while(1):
            if node.is_leaf():
                break
            # Greedily select next move.
            action, node = node.select(self._c_puct)
            state.do_move(action)

        # Evaluate the leaf using a network which outputs a list of
        # (action, probability) tuples p and also a score v in [-1, 1]
        # for the current player.
        action_probs, leaf_value = self._policy(state)
        # 判断游戏是否结束
        end, winner = state.game_end()
        if not end:
            node.expand(action_probs)
        else:
            # 如果结束,在叶节点中返回True
            if winner == -1:  # tie
                leaf_value = 0.0
            else:
                leaf_value = (1.0 if winner == state.get_current_player() else -1.0)

        # 更新节点中的各项值
        node.update_recursive(-leaf_value)

    def get_move_probs(self, state, temp=1e-3):
        """
        运行所有可能的情况,然后返回他们的概率
        temp: 该参数为(0, 1]中的数,用来控制计算深度
        """
        for n in range(self._n_playout):
            state_copy = copy.deepcopy(state)
            self._playout(state_copy)

        # 基于访问次数计算移动概率
        act_visits = [(act, node._n_visits)
                      for act, node in self._root._children.items()]
        acts, visits = zip(*act_visits)
        act_probs = softmax(1.0/temp * np.log(np.array(visits) + 1e-10))

        return acts, act_probs

    def update_with_move(self, last_move):
        """Step forward in the tree, keeping everything we already know
        about the subtree.
        """
        if last_move in self._root._children:
            self._root = self._root._children[last_move]
            self._root._parent = None
        else:
            self._root = TreeNode(None, 1.0)

    def __str__(self):
        return "MCTS"


class MCTSPlayer(object):
    """AI player based on MCTS"""

    def __init__(self, policy_value_function,
                 c_puct=5, n_playout=2000, is_selfplay=0):
        self.mcts = MCTS(policy_value_function, c_puct, n_playout)
        self._is_selfplay = is_selfplay

    def set_player_ind(self, p):
        self.player = p

    def reset_player(self):
        self.mcts.update_with_move(-1)

    def get_action(self, board, temp=1e-3, return_prob=0):
        sensible_moves = board.availables
        # the pi vector returned by MCTS as in the alphaGo Zero paper
        move_probs = np.zeros(board.width*board.height)
        if len(sensible_moves) > 0:
            acts, probs = self.mcts.get_move_probs(board, temp)
            move_probs[list(acts)] = probs
            if self._is_selfplay:
                # 自我训练函数
                move = np.random.choice(acts,p=0.75*probs + 0.25*np.random.dirichlet(0.3*np.ones(len(probs))))
                # 更新节点并重新训练
                self.mcts.update_with_move(move)
            else:
                # with the default temp=1e-3, it is almost equivalent
                move = np.random.choice(acts, p=probs)
                # 重置搜索树
                self.mcts.update_with_move(-1)

            if return_prob:
                return move, move_probs
            else:
                return move
        else:
            print("WARNING: the board is full")

    def __str__(self):
        return "MCTS {}".format(self.player)
