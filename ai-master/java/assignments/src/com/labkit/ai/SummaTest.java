/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.















path_to_goal: ['Up', 'Left', 'Left']
cost_of_path: 3
nodes_expanded: 10
fringe_size: 11
max_fringe_size: 12
search_depth: 3
max_search_depth: 4
running_time: 0.00188088
max_ram_usage: 0.07812500

 */
package com.labkit.ai;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

/**
 *
 * @author VDE
 */
public class SummaTest {

    public static void main(String[] args) {
      Integer[] initialState= new Integer[]{1,2,5,3,4,0,6,7,8}, goalState= new Integer[] {1,2,5,3,4,0,6,7,8};
      Set<PuzzleInstance> maxFrindge = new HashSet<> ();
      final PuzzleInstance initialStateInstance = new PuzzleInstance(initialState);
      final PuzzleInstance ins2 = new PuzzleInstance(goalState);
      
      maxFrindge.add(ins2);
      maxFrindge.add(initialStateInstance);
      System.out.println("The total size is "+maxFrindge.size());
    
    }
}
