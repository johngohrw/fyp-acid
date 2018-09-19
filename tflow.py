import tensorflow as tf

hello = tf.constant('what the fuck tensorflow')
sess = tf.Session()
print(sess.run(hello))