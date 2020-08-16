import numpy as np


def get_distribution(P):
	pmax = np.max(P)
	distribution=np.zeros(2048)
        interval =2048/pmax
	for i in P:
		index = int(np.fabs(i*interval))
		if index >= 2048:
			index = 2047
		distribution[index]= distribution[index] +1
	return distribution
def kl_divergence(P,Q,len):
	KL =0.0
	for i in range(len):
		try:
			if Q[i] == 0.0:
				KL = KL + 1		
			else:
				KL = KL+ P[i]*np.log(P[i]/Q[i])
		except:
			print 'Q:{},p:{}'.format(Q[i],P[i])
	return KL
def test():
	#P = np.random.rand(96*3*11*11)
	P = np.random.standard_normal(96*3*11*11)
	#Q = np.random.rand(96*3*11*11)
	Pdistribution = get_distribution(P)
        kl = np.inf
	for i in Pdistribution:
		if i ==0.0:
			print 'zeor'
	for k in range(128,2048):
		
		reference_distribution = Pdistribution[:k].copy()
		
		reference_distribution[k-1] = sum(Pdistribution[k::])
                interval = k/128.0
		#print interval
		quantized_distribution = np.zeros(k)
		
                for i in range(128):
			start = i*interval
			end   = (i+1)*interval
			
			leftupper  = int(np.ceil(start))
                        if leftupper > start:
				scale = leftupper-start
				quantized_distribution[i]  += scale * Pdistribution[leftupper-1]
			rightlower = int(np.floor(end))
		   	if rightlower < end:
				scale = end - rightlower
				quantized_distribution[i]  += scale * Pdistribution[rightlower]
				
			rightlower = int(np.floor(end))
			quantized_distribution[i] = sum(Pdistribution[leftupper:rightlower])
                expand_distribution = np.zeros(k)
		for i in range(128):
			start = i*interval
			end   = (i+1)*interval
			leftupper = int(np.ceil(start))
			count = 0
			if leftupper > start:
				count +=leftupper-start;
			rightlower =int(np.floor(end))
			if rightlower < end:
				count +=end -rightlower
			count = count+ rightlower - leftupper
			if count ==0:
				continue
			expandvalue = quantized_distribution[i]/count
			if leftupper > start and expand_distribution[leftupper-1] !=0:
				expand_distribution[leftupper-1] = expandvalue*(leftupper-start)
			if rightlower < end  and expand_distribution[rightlower] !=0:
				expand_distribution[rightlower] = expandvalue*(rightlower - end)
			expand_distribution[leftupper:rightlower] = expandvalue


		tempkl = kl_divergence(reference_distribution,expand_distribution,k)
		if tempkl < kl:
			kl = tempkl
			print 'kl :{},index:{}'.format(kl,k)
		#print 'kl :{},index:{}'.format(tempkl,k)
	
		#break

	return 
	

if __name__=="__main__":
	test()
