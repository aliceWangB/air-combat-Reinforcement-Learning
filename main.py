import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from class_env import AirCombat
CHECKPOINT_DIR = './checkpoint/'
EPOCH = 1002
MAX_STEPS = 1000
num_Action = 0
K = 0.5
alpha = 0.1
gamma = 0.4
EPSILON=0.1
#判断胜利失败函数

#ax = fig.add_subplot(111,projection='3d')  #这种方法也可以画多个子图
#创建网络模型
def net(input_state,labels):

    W1 = tf.Variable(tf.random_normal([72, 100], stddev=1, seed=1))
    b1 = tf.Variable(tf.zeros([100]))
    a1 = tf.nn.sigmoid(tf.matmul(input_state, W1) + b1)


    W2 = tf.Variable(tf.random_normal([100, 30], stddev=1, seed=1))
    b2 = tf.Variable(tf.zeros([30]))
    a2 = tf.nn.sigmoid(tf.matmul(a1, W2) + b2)

    W3 = tf.Variable(tf.random_normal([30, 9], stddev=1, seed=1))
    b3 = tf.Variable(tf.zeros([9]))
    y = tf.matmul(a2, W3) + b3
    loss = tf.reduce_mean(tf.square(labels - y))

    learning_rate = 0.1

    optimizer = tf.train.GradientDescentOptimizer(learning_rate)

    train_step = optimizer.minimize(loss)

    return train_step, loss, y

def greedy(prediction,list):
    temp = np.argmax(prediction)
    action = list[temp]
    return action


def main():
    #
    input = tf.placeholder("float32", [None,72])
    label = tf.placeholder("float32", [None, 9])
    #对一切先初始化
    train_step, loss, output = net(input, label)

    #NUMPY S0_A_List
    with tf.Session() as sess:
        saver = tf.train.Saver()
        sess.run(tf.global_variables_initializer())

        for num in range(EPOCH):
            X = []
            Y = []
            Z = []
            X_B = []
            Y_B = []
            Z_B = []
            print("第 %d 次游戏" % num)
            aircombat = AirCombat()
            position_r_0 = aircombat.position_r  # [1,8]
            x_r = position_r_0[0]
            y_r = position_r_0[1]
            z_r = position_r_0[2]
            X.append(x_r)
            Y.append(y_r)
            Z.append(z_r)

            position_b_0 = aircombat.position_b
            x_b = position_b_0[0]
            y_b = position_b_0[1]
            z_b = position_b_0[2]
            X_B.append(x_b)
            Y_B.append(y_b)
            Z_B.append(z_b)

            action_r_0 = aircombat.active_r
            action_b = aircombat.active_b
            # 态势使用两方的状态和动力学信息求出,下面是第一个态势
            s0 = aircombat.generate_state(position_r_0, position_b_0, action_r_0, action_b)
            # position_r_next, position_b_next = aircombat.generate_next_position(position_r_0, position_b_0,
            #                                                                    action_now=action_r_0)
            v_r = action_r_0[0]
            gamma_r = action_r_0[1]
            pusin_r = action_r_0[2]
            action_list = aircombat.action(v_r, gamma_r, pusin_r, flag=True, choose=1)
            action_b = aircombat.action_b(action_b)  # 匀速直线运动，即保持原先状态不动
            '''对于当前态势的所有动作结果，即网络的输入'''
            position_r_state1, position_b_state1 = aircombat.generate_next_position(position_r_0, position_b_0,
                                                                                    action_list[0],action_b)
            position_r_state2, position_b_state2 = aircombat.generate_next_position(position_r_0, position_b_0,
                                                                                    action_list[1],action_b)
            position_r_state3, position_b_state3 = aircombat.generate_next_position(position_r_0, position_b_0,
                                                                                    action_list[2],action_b)
            position_r_state4, position_b_state4 = aircombat.generate_next_position(position_r_0, position_b_0,
                                                                                    action_list[3],action_b)
            position_r_state5, position_b_state5 = aircombat.generate_next_position(position_r_0, position_b_0,
                                                                                    action_list[4],action_b)
            position_r_state6, position_b_state6 = aircombat.generate_next_position(position_r_0, position_b_0,
                                                                                    action_list[5],action_b)
            position_r_state7, position_b_state7 = aircombat.generate_next_position(position_r_0, position_b_0,
                                                                                    action_list[6],action_b)
            position_r_state8, position_b_state8 = aircombat.generate_next_position(position_r_0, position_b_0,
                                                                                    action_list[7],action_b)
            position_r_state9, position_b_state9 = aircombat.generate_next_position(position_r_0, position_b_0,
                                                                                    action_list[8],action_b)

            state_1 = aircombat.generate_state(position_r_state1, position_b_state1, action_list[0], action_b)
            state_2 = aircombat.generate_state(position_r_state2, position_b_state2, action_list[1], action_b)
            state_3 = aircombat.generate_state(position_r_state3, position_b_state3, action_list[2], action_b)
            state_4 = aircombat.generate_state(position_r_state4, position_b_state4, action_list[3], action_b)
            state_5 = aircombat.generate_state(position_r_state5, position_b_state5, action_list[4], action_b)
            state_6 = aircombat.generate_state(position_r_state6, position_b_state6, action_list[5], action_b)
            state_7 = aircombat.generate_state(position_r_state7, position_b_state7, action_list[6], action_b)
            state_8 = aircombat.generate_state(position_r_state8, position_b_state8, action_list[7], action_b)
            state_9 = aircombat.generate_state(position_r_state9, position_b_state9, action_list[8], action_b)
            state_1 = aircombat.normalize(state_1)
            state_2 = aircombat.normalize(state_2)
            state_3 = aircombat.normalize(state_3)
            state_4 = aircombat.normalize(state_4)
            state_5 = aircombat.normalize(state_5)
            state_6 = aircombat.normalize(state_6)
            state_7 = aircombat.normalize(state_7)
            state_8 = aircombat.normalize(state_8)
            state_9 = aircombat.normalize(state_9)

            start_input_list = [state_1, state_2, state_3, state_4, state_5, state_6, state_7, state_8, state_9]

            start_input_array = np.array(start_input_list)

            start_input = start_input_array.reshape((1,72))
            state_list = []
            state_list.append(start_input)

            r_list = []
            j = 0
            prediction_list = []
            state_list = []
            #labels_0 = np.zeros([9])
            #labels_0 = tf.convert_to_tensor(labels_0)
            state_now = start_input
            #action_list_now = action_list
            t_f = True
            while(t_f == True):#前向传播，生成结果
                prediction = sess.run(output,feed_dict={input:state_now})
                #print('prediction',prediction)
                prediction_list.append(prediction)
                temp = aircombat.epsilon_greedy(prediction,EPSILON)
                #temp = np.argmax(prediction)
                action_now = aircombat.action(v_r, gamma_r, pusin_r,flag=False,choose = temp)
                position_r_now,position_b_now = aircombat.generate_next_position(position_r_0, position_b_0,action_now,action_b)
                #position_r_now = aircombat.position_clip(position_r_now,position_b_now)
                state_next = aircombat.generate_state(position_r_now,position_b_now,action_now,action_b)

                v_r = action_now[0]
                gamma_r = action_now[1]
                pusin_r = action_now[2]
                action_list_now = aircombat.action(v_r, gamma_r, pusin_r, flag=True, choose=1)
                  # 匀速直线运动，即保持原先状态不动
                '''对于当前态势的所有动作结果，即网络的输入'''
                position_r_state1, position_b_state1 = aircombat.generate_next_position(position_r_now, position_b_now,
                                                                                        action_list_now[0],action_b)
                position_r_state2, position_b_state2 = aircombat.generate_next_position(position_r_now, position_b_now,
                                                                                        action_list_now[1],action_b)
                position_r_state3, position_b_state3 = aircombat.generate_next_position(position_r_now, position_b_now,
                                                                                        action_list_now[2],action_b)
                position_r_state4, position_b_state4 = aircombat.generate_next_position(position_r_now, position_b_now,
                                                                                        action_list_now[3],action_b)
                position_r_state5, position_b_state5 = aircombat.generate_next_position(position_r_now, position_b_now,
                                                                                        action_list_now[4],action_b)
                position_r_state6, position_b_state6 = aircombat.generate_next_position(position_r_now, position_b_now,
                                                                                        action_list_now[5],action_b)
                position_r_state7, position_b_state7 = aircombat.generate_next_position(position_r_now, position_b_now,
                                                                                        action_list_now[6],action_b)
                position_r_state8, position_b_state8 = aircombat.generate_next_position(position_r_now, position_b_now,
                                                                                        action_list_now[7],action_b)
                position_r_state9, position_b_state9 = aircombat.generate_next_position(position_r_now, position_b_now,
                                                                                        action_list_now[8],action_b)

                state_1 = aircombat.generate_state(position_r_state1, position_b_state1, action_list_now[0], action_b)
                state_2 = aircombat.generate_state(position_r_state2, position_b_state2, action_list_now[1], action_b)
                state_3 = aircombat.generate_state(position_r_state3, position_b_state3, action_list_now[2], action_b)
                state_4 = aircombat.generate_state(position_r_state4, position_b_state4, action_list_now[3], action_b)
                state_5 = aircombat.generate_state(position_r_state5, position_b_state5, action_list_now[4], action_b)
                state_6 = aircombat.generate_state(position_r_state6, position_b_state6, action_list_now[5], action_b)
                state_7 = aircombat.generate_state(position_r_state7, position_b_state7, action_list_now[6], action_b)
                state_8 = aircombat.generate_state(position_r_state8, position_b_state8, action_list_now[7], action_b)
                state_9 = aircombat.generate_state(position_r_state9, position_b_state9, action_list_now[8], action_b)
                state_1 = aircombat.normalize(state_1)
                state_2 = aircombat.normalize(state_2)
                state_3 = aircombat.normalize(state_3)
                state_4 = aircombat.normalize(state_4)
                state_5 = aircombat.normalize(state_5)
                state_6 = aircombat.normalize(state_6)
                state_7 = aircombat.normalize(state_7)
                state_8 = aircombat.normalize(state_8)
                state_9 = aircombat.normalize(state_9)
                start_input_now = [state_1, state_2, state_3, state_4, state_5, state_6, state_7, state_8, state_9]

                state_now = np.array(start_input_now)
                state_now = state_now.reshape((1, 72))
                state_list.append(state_now)
                q_r = state_next[0]
                q_b = state_next[1]
                d = state_next[2]
                delta_h = state_next[4]
                position_r_0 = position_r_now
                position_b_0 = position_b_now
                x_r = position_r_now[0]
                y_r = position_r_now[1]
                z_r = position_r_now[2]
                x_b = position_b_now[0]
                y_b = position_b_now[1]
                z_b = position_b_now[2]

                X.append(x_r)
                Y.append(y_r)
                Z.append(z_r)

                X_B.append(x_b)
                Y_B.append(y_b)
                Z_B.append(z_b)
                x_instance = abs(x_r-x_b)
                j+=1
                print('第%d步'%j)
                print('态势:',state_next)
                print('红方位置:',x_r,y_r,z_r)
                print('红方速度角度:',action_now)
                print('蓝方位置:',x_b,y_b,z_b)
                print('蓝方速度角度:',action_b)
                if j == MAX_STEPS:
                    print('达到最大步数')
                    t_f = False
                    R = -5
                if d<2500:
                    if q_r < 30 and q_b>30 and delta_h>100:
                        print('red win!')
                        t_f = False
                        R = 10
                    if q_r > 30 and q_b<30 and delta_h<100:
                        print('blue win...')
                        t_f = False
                        R = -10
                if x_r>200000 or x_r<0 or y_r>200000 or y_r<0 or z_r>11000 or z_r<0 or x_b>200000 or x_b<0 or y_b>200000 or y_b<0 or z_b>11000 or z_b<0:

                    print('超出作战范围')
                    t_f = False
                    R = -5
            X = np.array(X)
            Y = np.array(Y)
            Z = np.array(Z)
            X_B = np.array(X_B)
            Y_B = np.array(Y_B)
            Z_B = np.array(Z_B)

            #ax1.scatter3D(X, Y, Z, cmap='Blues')
            #ax1.plot3D(X, Y, Z, 'gray')
            #ax1.scatter3D(X_B, Y_B, Z_B, cmap='Reds')
            #plt.show()
            #记录一次学习过程中的所有回报，值函数等信息，以训练网络
            r_list = np.zeros(j)
            for i in range(j):
                r_list[i] = K**(j-i)*R
            delta = np.zeros_like(prediction_list)
            for k in range(j-1):
                delta[k] = prediction_list[k]+alpha*(r_list[k]+gamma*prediction_list[k+1]-prediction_list[k])
            delta[j - 1] = 0.01
            target = np.zeros_like(prediction_list)
            for k in range(j):
                target[k] = prediction_list[k] + delta[k]
            print('训练中')
            for i in range(j):#训练过程

                sess.run(tf.global_variables_initializer())
                sess.run(train_step,feed_dict={input:state_list[i],label:target[i]})
            if num==100 or num==200 or num==300 or num==400 or num==500 or num==1000:
                saver.save(sess,CHECKPOINT_DIR, global_step=num)
                print('Write checkpoint at %s' % num)

def test():
    input = tf.placeholder("float32", [None, 72])
    label = tf.placeholder("float32", [None, 9])
    # 对一切先初始化
    train_step, loss, output = net(input, label)
    with tf.Session() as sess:
        saver = tf.train.Saver()  # 常规操作，用于保存模型

        checkpoint = tf.train.get_checkpoint_state(CHECKPOINT_DIR)  # 找到最新的模型

        saver.restore(sess, checkpoint.model_checkpoint_path)
        fig = plt.figure()
        ax1 = plt.axes(projection='3d')
        X = []
        Y = []
        Z = []
        X_B = []
        Y_B = []
        Z_B = []
        aircombat = AirCombat()
        position_r_0 = aircombat.position_r  # [1,8]
        action_r_0 = aircombat.active_r
        position_b_0 = aircombat.position_b
        action_b = aircombat.active_b
        # 态势使用两方的状态和动力学信息求出,下面是第一个态势
        s0 = aircombat.generate_state(position_r_0, position_b_0, action_r_0, action_b)
        # position_r_next, position_b_next = aircombat.generate_next_position(position_r_0, position_b_0,
        #                                                                    action_now=action_r_0)
        v_r = action_r_0[0]
        gamma_r = action_r_0[1]
        pusin_r = action_r_0[2]
        action_list = aircombat.action(v_r, gamma_r, pusin_r, flag=True, choose=1)
        action_b = aircombat.action_b(action_b)  # 匀速直线运动，即保持原先状态不动
        '''对于当前态势的所有动作结果，即网络的输入'''
        position_r_state1, position_b_state1 = aircombat.generate_next_position(position_r_0, position_b_0,
                                                                                action_list[0], action_b)
        position_r_state2, position_b_state2 = aircombat.generate_next_position(position_r_0, position_b_0,
                                                                                action_list[1], action_b)
        position_r_state3, position_b_state3 = aircombat.generate_next_position(position_r_0, position_b_0,
                                                                                action_list[2], action_b)
        position_r_state4, position_b_state4 = aircombat.generate_next_position(position_r_0, position_b_0,
                                                                                action_list[3], action_b)
        position_r_state5, position_b_state5 = aircombat.generate_next_position(position_r_0, position_b_0,
                                                                                action_list[4], action_b)
        position_r_state6, position_b_state6 = aircombat.generate_next_position(position_r_0, position_b_0,
                                                                                action_list[5], action_b)
        position_r_state7, position_b_state7 = aircombat.generate_next_position(position_r_0, position_b_0,
                                                                                action_list[6], action_b)
        position_r_state8, position_b_state8 = aircombat.generate_next_position(position_r_0, position_b_0,
                                                                                action_list[7], action_b)
        position_r_state9, position_b_state9 = aircombat.generate_next_position(position_r_0, position_b_0,
                                                                                action_list[8], action_b)

        state_1 = aircombat.generate_state(position_r_state1, position_b_state1, action_list[0], action_b)
        state_2 = aircombat.generate_state(position_r_state2, position_b_state2, action_list[1], action_b)
        state_3 = aircombat.generate_state(position_r_state3, position_b_state3, action_list[2], action_b)
        state_4 = aircombat.generate_state(position_r_state4, position_b_state4, action_list[3], action_b)
        state_5 = aircombat.generate_state(position_r_state5, position_b_state5, action_list[4], action_b)
        state_6 = aircombat.generate_state(position_r_state6, position_b_state6, action_list[5], action_b)
        state_7 = aircombat.generate_state(position_r_state7, position_b_state7, action_list[6], action_b)
        state_8 = aircombat.generate_state(position_r_state8, position_b_state8, action_list[7], action_b)
        state_9 = aircombat.generate_state(position_r_state9, position_b_state9, action_list[8], action_b)
        state_1 = aircombat.normalize(state_1)
        state_2 = aircombat.normalize(state_2)
        state_3 = aircombat.normalize(state_3)
        state_4 = aircombat.normalize(state_4)
        state_5 = aircombat.normalize(state_5)
        state_6 = aircombat.normalize(state_6)
        state_7 = aircombat.normalize(state_7)
        state_8 = aircombat.normalize(state_8)
        state_9 = aircombat.normalize(state_9)
        start_input_list = [state_1, state_2, state_3, state_4, state_5, state_6, state_7, state_8, state_9]

        start_input_array = np.array(start_input_list)

        start_input = start_input_array.reshape((1, 72))
        state_list = []
        state_list.append(start_input)

        r_list = []
        j = 0
        prediction_list = []
        state_list = []
        # labels_0 = np.zeros([9])
        # labels_0 = tf.convert_to_tensor(labels_0)
        state_now = start_input

        # action_list_now = action_list
        t_f = True
        while (t_f == True):  # 前向传播，生成结果
            prediction = sess.run(output, feed_dict={input: state_now})
            # print('prediction',prediction)
            prediction_list.append(prediction)
            temp = np.argmax(prediction)
            action_now = aircombat.action(v_r, gamma_r, pusin_r, flag=False, choose=temp)
            position_r_now, position_b_now = aircombat.generate_next_position(position_r_0, position_b_0, action_now,
                                                                              action_b)

            state_next = aircombat.generate_state(position_r_now, position_b_now, action_now, action_b)

            v_r = action_now[0]
            gamma_r = action_now[1]
            pusin_r = action_now[2]
            action_list_now = aircombat.action(v_r, gamma_r, pusin_r, flag=True, choose=1)
            # 匀速直线运动，即保持原先状态不动
            '''对于当前态势的所有动作结果，即网络的输入'''
            position_r_state1, position_b_state1 = aircombat.generate_next_position(position_r_now, position_b_now,
                                                                                    action_list_now[0], action_b)
            position_r_state2, position_b_state2 = aircombat.generate_next_position(position_r_now, position_b_now,
                                                                                    action_list_now[1], action_b)
            position_r_state3, position_b_state3 = aircombat.generate_next_position(position_r_now, position_b_now,
                                                                                    action_list_now[2], action_b)
            position_r_state4, position_b_state4 = aircombat.generate_next_position(position_r_now, position_b_now,
                                                                                    action_list_now[3], action_b)
            position_r_state5, position_b_state5 = aircombat.generate_next_position(position_r_now, position_b_now,
                                                                                    action_list_now[4], action_b)
            position_r_state6, position_b_state6 = aircombat.generate_next_position(position_r_now, position_b_now,
                                                                                    action_list_now[5], action_b)
            position_r_state7, position_b_state7 = aircombat.generate_next_position(position_r_now, position_b_now,
                                                                                    action_list_now[6], action_b)
            position_r_state8, position_b_state8 = aircombat.generate_next_position(position_r_now, position_b_now,
                                                                                    action_list_now[7], action_b)
            position_r_state9, position_b_state9 = aircombat.generate_next_position(position_r_now, position_b_now,
                                                                                    action_list_now[8], action_b)

            state_1 = aircombat.generate_state(position_r_state1, position_b_state1, action_list_now[0], action_b)
            state_2 = aircombat.generate_state(position_r_state2, position_b_state2, action_list_now[1], action_b)
            state_3 = aircombat.generate_state(position_r_state3, position_b_state3, action_list_now[2], action_b)
            state_4 = aircombat.generate_state(position_r_state4, position_b_state4, action_list_now[3], action_b)
            state_5 = aircombat.generate_state(position_r_state5, position_b_state5, action_list_now[4], action_b)
            state_6 = aircombat.generate_state(position_r_state6, position_b_state6, action_list_now[5], action_b)
            state_7 = aircombat.generate_state(position_r_state7, position_b_state7, action_list_now[6], action_b)
            state_8 = aircombat.generate_state(position_r_state8, position_b_state8, action_list_now[7], action_b)
            state_9 = aircombat.generate_state(position_r_state9, position_b_state9, action_list_now[8], action_b)
            state_1 = aircombat.normalize(state_1)
            state_2 = aircombat.normalize(state_2)
            state_3 = aircombat.normalize(state_3)
            state_4 = aircombat.normalize(state_4)
            state_5 = aircombat.normalize(state_5)
            state_6 = aircombat.normalize(state_6)
            state_7 = aircombat.normalize(state_7)
            state_8 = aircombat.normalize(state_8)
            state_9 = aircombat.normalize(state_9)
            start_input_now = [state_1, state_2, state_3, state_4, state_5, state_6, state_7, state_8, state_9]

            state_now = np.array(start_input_now)
            state_now = state_now.reshape((1, 72))
            state_list.append(state_now)
            q_r = state_next[0]
            q_b = state_next[1]
            d = state_next[2]
            delta_h = state_next[4]
            position_r_0 = position_r_now
            position_b_0 = position_b_now
            x_r = position_r_now[0]
            y_r = position_r_now[1]
            z_r = position_r_now[2]
            x_b = position_b_now[0]
            y_b = position_b_now[1]
            z_b = position_b_now[2]

            X.append(x_r)
            Y.append(y_r)
            Z.append(z_r)

            X_B.append(x_b)
            Y_B.append(y_b)
            Z_B.append(z_b)

            j += 1
            print('第%d步' % j)
            print('态势:', state_next)
            print('红方位置:', x_r, y_r, z_r)
            print('红方速度角度:', action_now)
            print('蓝方位置:', x_b, y_b, z_b)
            print('蓝方速度角度:', action_b)
            if j == MAX_STEPS:
                print('达到最大步数')
                t_f = False
                R = -5
            if d < 2500:
                if q_r < 30 and q_b > 30 and delta_h>0:
                    print('red win!')
                    t_f = False
                    R = 10
                if q_r > 30 and q_b < 30 and delta_h<0:
                    print('blue win...')
                    t_f = False
                    R = -10
            if x_r > 200000 or x_r < 0 or y_r > 200000 or y_r < 0 or z_r > 11000 or z_r < 0 or x_b > 200000 or x_b < 0 or y_b > 200000 or y_b < 0 or z_b > 11000 or z_b < 0:
                print('超出作战范围')
                t_f = False
                R = -5
        X = np.array(X)
        Y = np.array(Y)
        Z = np.array(Z)
        X_B = np.array(X_B)
        Y_B = np.array(Y_B)
        Z_B = np.array(Z_B)

        ax1.scatter3D(X, Y, Z, cmap='Blues')
        ax1.plot3D(X, Y, Z, 'gray')
        ax1.scatter3D(X_B, Y_B, Z_B, cmap='Reds')
        plt.show()
        # 记录一次学习过程中的所有回报，值函数等信息，以训练网络
if __name__ == '__main__':
    main()
    #test()



