import random

class OperandsSamplerBase:
    def __init__(self,num_operands):
        self.n = num_operands
        
    def sample(self):
         raise NotImplementedError("Subclass must implement abstract method")
            
    def get_operands_basics(self):
        ops_list = []
        
        for i in range(self.n):
            ops = [1000]*self.n
            ops[i] = 10
            ops_list.append(ops)
            
        for i in range(self.n):
            ops = [10]*self.n
            ops[i] = 1000
            ops_list.append(ops)
        
        
        xx = [100,300,500,1000,1500]
        
        for x in xx:
            ops = [x]*self.n
            ops_list.append(ops)
            
        yy = [10,50,70]
        for y in yy:
            ops = [y]*self.n
            ops_list.append(ops)
        
        return ops_list

class OperandsSamplerCorner(OperandsSamplerBase):
    def __init__(self,num_operands, max_op_size, corner,p_corner,seed=108):
        super().__init__(num_operands)
        self.seed = seed
        self.max_op = max_op_size
        self.corner = corner
        
        assert 0<= p_corner <=1, "p_corner should be between 0 and 1"
        assert 1 <= corner <=0.1*max_op_size, "corner should be an integer val between 0 and 10 percernt of max op size"
        
        self.p = p_corner
        random.seed(self.seed)
        
    def sample(self):
        
        p1 = random.random()
        if p1 < self.p:
            ops = self.sample_corner()
        else:
            p3 = random.random()
            if p3 < 0.8: 
                ops = self.sample_normal_1()
            else:
                ops = self.sample_normal_2()
            
        return ops
    
    def sample_corner(self):
        ops = self.sample_normal_1()
        idx = random.sample(range(self.n),1)[0]
        ops[idx] = random.randint(1,self.corner)
        return ops
        
    def sample_normal_1(self):
        ops = []
        for i in range(self.n):
            ops.append(random.randint(self.corner,self.max_op))
        return ops
    
    def sample_normal_2(self):
        ops = []
        for i in range(self.n):
            ops.append(random.randint(1,self.max_op))
        return ops


    