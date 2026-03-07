import tensorflow as tf

class BoothLayer(tf.keras.layers.Layer):
    def __init__(self, bits=8, **kwargs):
        super(BoothLayer, self).__init__(**kwargs)
        self.bits = bits

    def call(self, inputs):
        # inputs = [multiplicand, multiplier]
        m, q = tf.cast(inputs[0], tf.int32), tf.cast(inputs[1], tf.int32)
        mask = (1 << self.bits) - 1
        
        a = tf.zeros_like(m)
        q_prev = tf.zeros_like(m)
        
        for _ in range(self.bits):
            # Decision Logic using bitwise ops
            # (Simplified for clarity: in TF you use tf.bitwise)
            cond = (q & 1) - q_prev
            a = tf.where(cond == 1, (a - m) & mask, a)
            a = tf.where(cond == -1, (a + m) & mask, a)
            
            # Arithmetic Right Shift
            new_q_prev = q & 1
            q = (q >> 1) | ((a & 1) << (self.bits - 1))
            a = tf.bitwise.right_shift(a, 1) # Note: requires careful sign handling
            q_prev = new_q_prev
            
        return tf.cast((a << self.bits) | q, tf.float32)
