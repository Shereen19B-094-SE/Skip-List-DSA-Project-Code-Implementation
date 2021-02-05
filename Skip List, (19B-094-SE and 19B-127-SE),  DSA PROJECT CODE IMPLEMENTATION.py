#!/usr/bin/env python
# coding: utf-8

# In[2]:


import random 
  
class Node: #Class used to create a node for the  skip list

    def __init__(self, value, level): 
        self.value = value 
  
        # This list will hold references to nodes on different levels 
        self.forward = [None]*(level+1) 
        
        
class SkipList: #Class to create a skiplist having a certain number of levels and probability of the level of a new node

    def __init__(self, max_lvl, P): 
        # Maximum level for this skip list 
        self.max_lvl= max_lvl 
  
    #The skip list has  a probability p associated with it, where 0<p<1. This determines the probability 
                                                                            #of the level of a new node
    #When creating a new node, flip a coin that has probability p of heads
    
    #Count the number of heads before the first tails that occurred, plus one: this value is the level of the new node
    
    #For example, with P=1/2, the probability of a new node being level 1 is 1/2; 
    #of being level 2 is 1/4; of being level 3 is 1/8; etc

        self.P = P 
  
        # create header node and initialize key to -1 
        self.header = self.createNode(self.max_lvl , -1) 
  
        # pointer to indicate current level of skip list 
        self.level = 0
      
    # create  new node 
    def createNode(self, lvl, value): 
        n = Node(value, lvl) 
        return n 
      
    # create random level for node 
    def randomLevel(self): 
        lvl = 0
        while random.random()<self.P and lvl<self.max_lvl:
            lvl += 1
        return lvl 
    
    # Function to insert a key in the skip list 
    def Insert(self, value): 
        # create update array and initialize it 
        update = [None]*(self.max_lvl +1) #The update array will be storing the pointers that point to such nodes
                                        #whose forward pointers might need to be updated to point to a newly inserted node
        current = self.header 
  
         
        #We start from highest level of skip list and  
        #move the current reference forward, while key  
        #is greater than key of node next to current node.
        
        #Otherwise, the current will be inserted into the update array and  
        #then we move one level down and continue searching linearly for such a current node whose
        #next node's key is greater than the key we're inserting
        
        for i in range(self.level, -1, -1): 
            while current.forward[i] and current.forward[i].value < value: 
                current = current.forward[i] 
            update[i] = current 
  
        
        #If current node's next node's key is greater than key to be inserted
        #and we are at lowest level (level 0), then we have found the ideal place for the key to be inserted
         
        current = current.forward[0] 
  
        
        #If current node is NULL, then this means we have reached 
           #the end of the level or in other words, current's key is not equal 
           #to key to insert that means we have to generate a random level for the key to be inserted into.
        #(The level of a node is determined by a random number generator when the node is created)
       
        if current == None or current.value != value: 
            # Generate a random level for node 
            rlevel = self.randomLevel() 
  
            
            #If random level is greater than list's current 
            #level, then initialize update value with reference 
            #to header for further use 
            
            if rlevel > self.level: 
                for i in range(self.level+1, rlevel+1): 
                    update[i] = self.header 
                self.level = rlevel 
  
            # create new node with random level generated 
            n = self.createNode(rlevel, value) 
  
            # insert node by rearranging references  
            for i in range(rlevel+1): 
                n.forward[i] = update[i].forward[i] 
                update[i].forward[i] = n 
            print("The value {} has been inserted.".format(value)) 
            print("")
                
    def Delete(self, search_value): 
        #The update array is important here too: it keeps track of nodes whose pointers may
        #need to change to “unsplice” the to-be-deleted node

            # create update array and initialize it 
            update = [None]*(self.max_lvl+1) 
            current = self.header 

             
            #We start from highest level of skip list and
            #move the current reference forward, while the value 
            #is greater than value of node next to current.
            #Otherwise, the current node gets inserted into update[] and  
            # we move one level down and continue searching linearly for the node that needs to be deleted
            
            for i in range(self.level, -1, -1): 
                while(current.forward[i] and current.forward[i].value < search_value): 
                    current = current.forward[i] 
                update[i] = current 

              
            #Reached level 0 and advanced reference to node on the
            #right, which is possibly the node we want to delete 
             
            current = current.forward[0] 

            
            if current != None and current.value == search_value: # If current node is the node to be deleted

                
                #The we start from lowest level and rearrange references  
                #just as it is done in a singly linked list
                #when removing a particular node.
            
                for i in range(self.level+1): 

                    
                    #If at level i, next node is not target  
                    #node, break the loop, and do not need move to a further level 
                    
                    if update[i].forward[i] != current: 
                        break
                    update[i].forward[i] = current.forward[i] 

                # If there are levels that no longer have any elements residing in it, then remove those levels
                while(self.level>0 and self.header.forward[self.level] == None): 
                    self.level=self.level-1
                print("Successfully deleted {}".format(search_value)) 
                
                
                
#We want to search for a node of a specific value , so we start from first node of “express lane”/ uppermost level
#and keep moving on “express lane” until we 
#find a node that has a next node value greater than the value we are looking for. 

#Once we find such a node on “express lane”,we move to “normal lane”/lower level using a pointer from this node, 
#and linearly search for 50 on “normal lane”. 

#Specifically, we start from highest level of the skip list 
        #and move the current reference forward while the value of the node  
        #is greater than the current node's next node's value.
#Otherwise, move one level down and continue searching 
  
    def Search(self, value):  
        current = self.header
 
        
        for i in range(self.level, -1, -1): 
            while(current.forward[i] and current.forward[i].value < value): 
                current = current.forward[i] 
  
        # reached level 0 and advance reference to  
        # right, which is prssibly our desired node 
        current = current.forward[0] 
  
        # If current node have key equal to 
        # search key, we have found our target node 
        if current and current.value == value: 
            print("Found the key: {} ".format(value))
            
            
            
    def PrintSkipList(self): 
        print("\n----Skip List----") 
        head = self.header 
        
        for lvl in range(self.level+1): 
            print("Level {}: ".format(lvl), end=" ")
            node = head.forward[lvl] 
           
            while(node != None): 
                print(node.value, end=" ") 
                node = node.forward[lvl] 
            print("")
            

#DRIVER CODE:
skip_lst = SkipList(3, 0.5) 
skip_lst.Insert(3) 
skip_lst.Insert(6) 
skip_lst.Insert(7) 
skip_lst.Insert(9) 
skip_lst.Insert(12) 
skip_lst.Insert(19) 
skip_lst.Insert(17) 
skip_lst.Insert(26) 
skip_lst.Insert(21) 
skip_lst.Insert(25) 

skip_lst.PrintSkipList() 
  
# Search for node 21
skip_lst.Search(21) 
  
# Delete node 21 
skip_lst.Delete(21) 

print("")
print("")
print("The Skip List After Deletion:")
skip_lst.PrintSkipList() 
            


# In[ ]:




