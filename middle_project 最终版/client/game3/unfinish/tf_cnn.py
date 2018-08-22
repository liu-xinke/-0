'''
此文件利用tensorflow模块搭建神经网络

CNN卷积神经网络包含以下几层：
    ● 输入层：用于数据的输入
    ● 卷积层：使用卷积核进行特征提取和特征映射
    ● 激励层：由于卷积也是一种线性运算，因此需要增加非线性映射
    ● 池化层：进行下采样，对特征图稀疏处理，减少数据运算量。
    ● 全连接层：通常在CNN的尾部进行重新拟合，减少特征信息的损失
    ● 输出层：用于输出结果

tensorflow模块安装:sudo pip3 install --user tensorflow==1.9.0rc2
tensorflow模块参考资料:https://www.w3cschool.cn/tensorflow_python/
'''

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf



class PolicyValueNet():
    def __init__(self):
        tf.reset_default_graph() #初始化图像
        self.board_width = 15   #棋盘大小
        self.board_height = 15
        self.model_file = './model/tf_policy_5_model' # 文件用于保存计算模型
        self.sess = tf.Session()  #创建类对象
        self.l2_const = 1e-4      #coef of l2 penalty 
        self._create_policy_value_net() 
        self._loss_train_op()
        self.saver = tf.train.Saver() # 模型保存
        self.restore_model()      # 模型重载/继续训练
            
    def _create_policy_value_net(self):
        """创建神经网络"""
        # 输入层
        with tf.name_scope("inputs"):
            #tf.placeholder 一般用作占位
            self.state_input = tf.placeholder(tf.float32, shape=[None, 4, self.board_width, self.board_height], name="state")

            self.winner = tf.placeholder(tf.float32, shape=[None], name="winner") 
            self.winner_reshape = tf.reshape(self.winner, [-1,1])  # tf.reshape 调整矩阵维度 第1个参数为被调整维度的张量，第2个参数为要调整为的形状。
            self.mcts_probs = tf.placeholder(tf.float32, shape=[None, self.board_width*self.board_height], name="mcts_probs")
        
        # 卷积层
        # activation 激活函数选项
        # 激活函数参考资料:https://blog.csdn.net/qq_27248897/article/details/77071027
        conv1 = tf.layers.conv2d(self.state_input, filters=32, kernel_size=3,
                         strides=1, padding="SAME", data_format='channels_first',
                         activation=tf.nn.relu, name="conv1")
        conv2 = tf.layers.conv2d(conv1, filters=64, kernel_size=3,
                         strides=1, padding="SAME", data_format='channels_first',
                         activation=tf.nn.relu, name="conv2")               
        conv3 = tf.layers.conv2d(conv2, filters=128, kernel_size=3,
                         strides=1, padding="SAME", data_format='channels_first',
                         activation=tf.nn.relu, name="conv3")
        
        # 激励层
        policy_net = tf.layers.conv2d(conv3, filters=4, kernel_size=1,
                         strides=1, padding="SAME", data_format='channels_first',
                         activation=tf.nn.relu, name="policy_net")
        policy_net_flat = tf.reshape(policy_net, shape=[-1, 4*self.board_width*self.board_height])
        self.policy_net_out = tf.layers.dense(policy_net_flat, self.board_width*self.board_height, name="output")
        self.action_probs = tf.nn.softmax(self.policy_net_out, name="policy_net_proba")

        # 全连接层
        value_net = tf.layers.conv2d(conv3, filters=2, kernel_size=1, data_format='channels_first',
                                     name='value_conv', activation=tf.nn.relu)
        value_net = tf.layers.dense(tf.contrib.layers.flatten(value_net), 64, activation=tf.nn.relu)
        self.value = tf.layers.dense(value_net, units=1, activation=tf.nn.tanh)
    
    def _loss_train_op(self):
        """
        损失函数计算 
        损失函数参考资料:https://blog.csdn.net/willduan1/article/details/73694826
        loss = (z - v)^2 + pi^T * log(p) + c||theta||^2
        """
        l2_penalty = 0
        for v in tf.trainable_variables():
            if not 'bias' in v.name.lower():
                l2_penalty += tf.nn.l2_loss(v)
        value_loss = tf.reduce_mean(tf.square(self.winner_reshape - self.value))
        cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=self.policy_net_out, labels=self.mcts_probs)
        policy_loss = tf.reduce_mean(cross_entropy)
        self.loss =  value_loss + policy_loss + self.l2_const*l2_penalty
        # policy entropy，for monitoring only
        self.entropy = policy_loss
        # get the train op   
        self.learning_rate = tf.placeholder(tf.float32)
        optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
        self.training_op = optimizer.minimize(self.loss)
        
    def get_policy_value(self, state_batch):
         # 获取动作概率和得分值
        action_probs, value = self.sess.run([self.action_probs, self.value],
                                    feed_dict={self.state_input: state_batch})       
        return action_probs, value

    def policy_value_fn(self, board):
        """输出层"""
        legal_positions = board.availables
        current_state = board.current_state()
        act_probs, value = self.sess.run([self.action_probs, self.value], 
                                    feed_dict={self.state_input: current_state.reshape(-1, 4, self.board_width, self.board_height)})
        act_probs = zip(legal_positions, act_probs.flatten()[legal_positions])
        return act_probs, value[0][0]
        
    def train_step(self, state_batch, mcts_probs_batch, winner_batch, lr):
        feed_dict = {self.state_input : state_batch,
                     self.mcts_probs : mcts_probs_batch, 
                     self.winner : winner_batch,
                     self.learning_rate: lr}

        loss, entropy, _ = self.sess.run([self.loss, self.entropy, self.training_op],
                                     feed_dict=feed_dict)
        return loss, entropy

    
    def restore_model(self):        
        if os.path.exists(self.model_file + '.meta'):
            self.saver.restore(self.sess, self.model_file)
        else:
            self.sess.run(tf.global_variables_initializer())
