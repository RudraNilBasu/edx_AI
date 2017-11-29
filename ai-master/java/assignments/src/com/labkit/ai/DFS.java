package com.labkit.ai;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;
import java.util.Set;

/**
 *
 *  Implementation of Depth first search algorithm 
 * @author vidhyadharan (it.vidhyadharan@gmail.com)
 */
public class DFS {
    
    
    public static void main(String[] args) {
        
       Integer[] initialState= new Integer[]{1,2,5,3,4,0,6,7,8}, goalState= new Integer[] {0,1,2,3,4,5,6,7,8};
       
       LinkedList<PuzzleInstance> frontier = new LinkedList<>();
       
        long startTime = System.currentTimeMillis();
       final PuzzleInstance GOALSTATE = new PuzzleInstance(goalState);
       final PuzzleInstance initialStateInstance = new PuzzleInstance(initialState);
       
       Set<PuzzleInstance> maxFrindge = new HashSet<> ();
       maxFrindge.add(initialStateInstance);
       
       frontier.add(initialStateInstance);
       int nodes_expanded =0;
       int max_frindge_size = frontier.size();
       while(!frontier.isEmpty()){
           PuzzleInstance firstElement = frontier.poll();
           if(firstElement.equals(GOALSTATE)){
                printOutPut(firstElement);
               break;
           }else{
//               System.out.println("Traversing");
               /** reverse the UDLR ordering to RLDU */
               List<PuzzleInstance> possibleNextMoves = firstElement.generateInstance();
               Collections.reverse(possibleNextMoves);
               System.out.println("possibleNextMoves = " + possibleNextMoves);
               
               possibleNextMoves.forEach((PuzzleInstance possibleNextMove) -> {
                   if(maxFrindge.add(possibleNextMove)){// if it is true then the next move is valid
                       frontier.addFirst(possibleNextMove);
                   }else {
                       System.out.println("Already traversed , Hence skipping ");
                   }
               });
           }
           nodes_expanded++;
           if(frontier.size()>max_frindge_size){
               max_frindge_size = frontier.size();
           }
       }
        long endTime = System.currentTimeMillis();
  
    System.out.println("nodes_expanded :" + nodes_expanded);    
    System.out.println("fringe_size: " + frontier.size());
    System.out.println("max_fringe_size: "+max_frindge_size);
    System.out.println("Total time = " + ((endTime - startTime)));
    }

    private static void printOutPut(PuzzleInstance firstElement) {
        System.out.println("Found the element");
        System.out.println(Arrays.toString(firstElement.getNumbers()));
       
         ArrayList<String> pathToGoal,list = new ArrayList<>(10);
        pathToGoal = getPathToGoal(list,firstElement);
//         Collections.reverse(pathToGoal);
        System.out.println("path_to_goal: "+pathToGoal);
         System.out.println("cost_of_path :"+firstElement.getCostOfPath());
    }

    private static ArrayList<String> getPathToGoal(ArrayList<String> list ,PuzzleInstance firstElement) {
        PuzzleInstance child = firstElement;
        Boolean isNextAvailable = (child.getParent() != null);
        while(isNextAvailable){
            
            String direction = child.getDirection();
           list.add(direction);
           PuzzleInstance parent = child.getParent();
           isNextAvailable = (parent.getParent() != null);
           PuzzleInstance garbage = child;
           child = parent;
        } 
        return list;
    }
    
    
}
