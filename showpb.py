import tensorflow as tf
from tensorflow.python.framework import tensor_util
import os

def show():
	
	output_graph = tf.GraphDef()
	output_graph_path  = os.sys.argv[1]
        
	
	#output_graph_path = '/home/xg/distccgo/model-mobilenet_v1_075.pb'
	with open(output_graph_path,"rb") as f:
		output_graph.ParseFromString(f.read())
        
      
        for node in output_graph.node:
		print 'name:{}'.format(node.name)
		print 'shape:{},dtype;{}'.format(node.attr['value'].tensor.tensor_shape,node.attr['value'].tensor.dtype)
		if node.attr['value'].tensor.dtype != 1:
			continue
		print tensor_util.MakeNdarray(node.attr['value'].tensor)
		
	
	


if __name__ == '__main__':
	show()

