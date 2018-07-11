from models.vgg16 import VGG16
from utils.load_weights import weight_loader
from pkl_reader import DataGenerator
import tensorflow as tf


def top5_acc(pred, k=5):
    Inf = 0.
    results = []
    for i in range(k):
        results.append(pred.index(max(pred)))
        pred[pred.index(max(pred))] = Inf
    return results


if __name__ == '__main__':
    weights = weight_loader('./weights/vgg16_weights_tf_dim_ordering_tf_kernels.h5', by_name=True)

    X = tf.placeholder(tf.float32, [None, 224, 224, 3])
    Y = tf.placeholder(tf.float32, [None, 1000])

    dg = DataGenerator('./data/val224_compressed.pkl', model='vgg', dtype='float32')
    with tf.device('/cpu:0'):
        logits = VGG16(X, weights)
        prediction = tf.nn.softmax(logits)

    acc = 0.
    acc_top5 = 0.
    with tf.Session() as sess:
        for im, label in dg.generator():
            out = sess.run(prediction, feed_dict={X: im})
            pred = tf.argmax(out, 1)
            if pred == label:
                acc += 1
            if label in top5_acc(out.tolist()):
                acc_top5 += 1
        print('Top1 accuracy: {}'.format(acc / 50000))
        print('Top5 accuracy: {}'.format(acc_top5 / 50000))