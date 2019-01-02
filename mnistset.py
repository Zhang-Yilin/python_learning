from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
import os

INPUT_NODE = 784
OUTPUT_NODE = 10
LAYER1_NODE = 500
LAYER2_NODE = 300
LAYER3_NODE = 100
BATCH_SIZE = 128
LEARNING_RATE = 0.001
REGULARIZER = 0.001
DECAY = 0.99
STEP = 50000
MODEL_SAVE_PATH="./test/"
MODEL_NAME="mnist_model"


def forward(x, regularize):
    w1 = get_w([INPUT_NODE, LAYER1_NODE], regularize)
    b1 = get_b([LAYER1_NODE])
    x1 = tf.nn.relu(tf.matmul(x, w1) + b1)
    w2 = get_w([LAYER1_NODE, LAYER2_NODE], regularize)
    b2 = get_b([LAYER2_NODE])
    x3 = tf.nn.relu(tf.matmul(x1, w2) +b2)
    w3 = get_w([LAYER2_NODE, LAYER3_NODE], regularize)
    b3 = get_b([LAYER3_NODE])
    y = tf.matmul(x3, w3) +b3
    return y

def get_w(shape, regularize, stddev = 0.1):
    w = tf.Variable(tf.truncated_normal(shape, stddev= stddev))
    if regularize != None:
        tf.add_to_collection("losses", tf.contrib.layers.l2_regularizer(regularize)(w))
    return w

def get_b(shape):
    b = tf.Variable(tf.zeros(shape))
    return b



def backward(mnist):
    x = tf.placeholder(tf.float32, [None, INPUT_NODE])
    y_ = tf.placeholder(tf.float32, [None, OUTPUT_NODE])
    y = forward(x, REGULARIZER)
    global_step = tf.Variable(0, trainable=False)

    ce = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y, labels=tf.argmax(y_, 1))
    cem = tf.reduce_mean(ce)
    loss = cem + tf.add_n(tf.get_collection("losses"))

    rate = tf.train.exponential_decay(LEARNING_RATE, global_step, mnist.train.num_examples/BATCH_SIZE,
                                      DECAY,staircase=True)

    train_step = tf.train.AdamOptimizer(rate).minimize(loss, global_step=global_step)

    saver = tf.train.Saver()

    predict = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(predict, tf.float32))

    with tf.Session() as sess:
        init_op = tf.global_variables_initializer()
        sess.run(init_op)

        for i in range(STEP):
            xs, ys = mnist.train.next_batch(BATCH_SIZE)
            _, loss_value, step = sess.run([train_step, loss, global_step], feed_dict={x:xs, y_:ys})
            if i % 1000 == 0:
                saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME), global_step= global_step)
                accuracy_score = sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels})
                print("step: %d, loss: %g, accuracy: %g" % (step, loss_value, accuracy_score))

def main():
    mnist = input_data.read_data_sets("./data/", one_hot=True)
    backward(mnist)

if __name__ == "__main__":
    main()