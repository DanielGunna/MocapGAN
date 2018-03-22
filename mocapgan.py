
from skeleton import Skeleton

class MocapGAN:
    
    def __init__(self):
        print ('Initializing')

    def read_file(self,file):
        file_skeleton = Skeleton(file,0.5)
   
    
         


if __name__ == '__main__':
    mocap = MocapGAN();
    mocap.read_file('example.bvh')

    




