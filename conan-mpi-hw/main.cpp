/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   main.cpp
 * Author: slange
 *
 * Created on 15 March 2018, 11:31
 */

#include <cstdlib>
#include "mpi.h"
#include <stdio.h>
#include <cstdio>
#include <string.h>
#include <iostream>


using namespace std;

/*
 * 
 */
int main(int argc, char** argv){
  int myrank, size;
  myrank = 0;
  size = 1;

  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  cout << "Rank " << myrank << " of " << size << " says: Hello World! \n";

  return 0;
}

