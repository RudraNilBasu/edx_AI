/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.labkit.ai;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 *
 * @author VDE
 */
public class PuzzleInstance {

    private final Integer[][] puzzle ;
    private final Integer rowColoumSize;
    private int row, coloum;
    private int cost_of_path=0;
    private String direction;
    private PuzzleInstance parent;

    public PuzzleInstance(Integer[][] puzzleAsMultiDimention,Integer rowColoumSize,int costOfPath, String dir, PuzzleInstance instance) {
        this.rowColoumSize = rowColoumSize;
        puzzle = new Integer[rowColoumSize][rowColoumSize];
        
        for (int i = 0; i < rowColoumSize; i++) 
        for (int j = 0; j < rowColoumSize; j++) {
              if(puzzleAsMultiDimention[i][j]==0){
                  this.row = i;
                  this.coloum=j;
                }
              this.puzzle[i][j] = puzzleAsMultiDimention[i][j].intValue();
           }
        
        cost_of_path = costOfPath;
        direction = dir;
        this.parent = instance;
    }

    public Integer[] getNumbers(){
        Integer [] asArray = new Integer[rowColoumSize*rowColoumSize];
        
          for (int i = 0, idx = 0; i < rowColoumSize; i++) {
            for (int j = 0; j < rowColoumSize; j++) {
                asArray[idx] = this.puzzle[i][j];
                idx++;
            }
        }
          return asArray;
        
    }
    public PuzzleInstance(Integer[] puzzle1Dimentional) {

        if (puzzle1Dimentional.length <= 0) {
            throw new RuntimeException("Length not met the criteria");
        }
        Double sqrt = Math.sqrt(puzzle1Dimentional.length);
        rowColoumSize = sqrt.intValue() ;
        
        this.puzzle = new Integer[rowColoumSize][rowColoumSize];

        for (int i = 0, idx = 0; i < rowColoumSize; i++) {
            for (int j = 0; j < rowColoumSize; j++) {
                this.puzzle[i][j] = puzzle1Dimentional[idx];
                //find the empty position and store the idex position
                if (puzzle1Dimentional[idx] == 0) {
                    row = i;
                    coloum = j;
                }
                idx++;
            }
        }

    }

    @Override
    public int hashCode() {
        int hash = 5;
        return hash;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null) {
            return false;
        }
        if (getClass() != obj.getClass()) {
            return false;
        }
        final PuzzleInstance other = (PuzzleInstance) obj;
        return Arrays.deepEquals(this.puzzle, other.puzzle);
    }

    /**
     * This will generate based on UDLR - Up, Down, Left, Right
     *
     * @return
     */
    public List<PuzzleInstance> generateInstance() {

        final String[] POSITION = {"Up", "Down", "Left", "Right"};// In this order
        List<PuzzleInstance> puzzleInstances = new ArrayList<>();

        for (String traverse : POSITION) {
            int tempI=-1, tempJ=-1;
            switch (traverse) {
                case "Up":
                    tempI = row - 1;                    
                    tempJ = coloum;
                    break;
                case "Down":
                    tempI = row + 1;                    
                    tempJ = coloum;
                    break;
                case "Left":
                    tempI = row;                    
                    tempJ = coloum - 1;
                    break;
                case "Right":
                    tempI = row;                    
                    tempJ = coloum + 1;
                    break;
            }
            
        if((tempI < 0 || tempJ <0)|| (tempI >= rowColoumSize || tempJ >=rowColoumSize )){
            System.out.println("Out of bound");
            // skip it nothing to add in the list
        }else{
            final Integer[][] puzzleGenerator = cloneArray(puzzle); 
            int temp = puzzleGenerator [tempI][tempJ];
            puzzleGenerator[tempI][tempJ] = 0;
            puzzleGenerator[row][coloum] = temp;
            
            PuzzleInstance puzzleInstance = new PuzzleInstance(cloneArray(puzzleGenerator),rowColoumSize,cost_of_path+1,traverse, this);
            puzzleInstances.add(puzzleInstance);         
         }
      }

        return puzzleInstances;
       
       
    }

    @Override
    public String toString() {
        return "PuzzleInstance{" + "puzzle=" + Arrays.deepToString(puzzle)+ ", direction=" + direction + '}';
    }

    public String getDirection() {
        return direction;
    }


    public PuzzleInstance getParent() {
        return parent;
    }
    
    
     public static Integer[][] cloneArray(Integer[][] src) {
        int length = src.length;
        Integer[][] target = new Integer[length][src[0].length];
        for (int i = 0; i < length; i++) {
            System.arraycopy(src[i], 0, target[i], 0, src[i].length);
        }
        return target;
    }

    public int getCostOfPath() {
       return cost_of_path;
    }

}
