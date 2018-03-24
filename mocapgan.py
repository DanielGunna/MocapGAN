
from skeleton import Skeleton
import numpy

class MocapGAN:
    
    def __init__(self):
        print ('Initializing')
        self.XtranIndex = 0
        self.YtranIndex = 1
        self.ZtranIndex = 2
        self.XrotIndex = 3
        self.YrotIndex = 4
        self.ZrotIndex = 5
        

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
        print (skeleton.root.frames[1])
        for i in range(0,len(joint_labels)):
            label = joint_labels[i]
            if 'EndEffector_' in label:
                joint = skeleton.getJoint(label.split('_')[1]).children[0]        
                print(joint.offset)
            else:
                joint = skeleton.getJoint(joint_labels[i])
                        
            
        
            
        
        
    def get_children_joint_labels(self,labels,joint):
    
        if joint.name == 'End effector':
            labels.append('EndEffector_' + joint.parent.name)
        else:
            labels.append(joint.name)
        for child in joint.children:
            self.get_children_joint_labels(labels,child)
        
    
    def start(self):
        self.build_skeleton_matrix(self.read_file("example.bvh"))
        
    

    
        
   
         


if __name__ == '__main__':
    mocap = MocapGAN();
    mocap.start()

    




