
from skeleton import Skeleton
import numpy

class MocapGAN:
    
    def __init__(self):
        print ('Initializing')

    def read_file(self,file):
        file_skeleton = Skeleton(file,0.5)
        return file_skeleton;
    
    def build_skeleton_matrix(self,skeleton):
        joint_labels = []
        self.get_children_joint_labels(joint_labels,skeleton.root)
        skeleton_matrix = numpy.zeros((
                len(joint_labels),
                6,
                skeleton.frames
        ));
       # for label,i in joint_labels,range(0,37):
        #    print (label.name +" "+ i)
                        
            
        
        
    def get_children_joint_labels(self,labels,joint):
    
        if joint.name == 'End effector':
            labels.append('EndEffector' + joint.parent.name)
        else:
            labels.append(joint.name)
        for child in joint.children:
            self.get_children_joint_labels(labels,child)
        
    
    def start(self):
        self.build_skeleton_matrix(self.read_file("example.bvh"))
        
    

    
        
   
         


if __name__ == '__main__':
    mocap = MocapGAN();
    mocap.start()

    




