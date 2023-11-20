'''Module for training and implementing models'''

#import modules
import collections
import itertools
import numpy as np
import typing

#functions
def get_amp_output(ic: np.ndarray, comms: typing.Tuple[int, int]) -> list:
    '''Returns amp output for phase setting and signal: (setting, sig).'''
    ix = 0
    id_ix = 0
    diag_codes = []

    while ix < len(ic):
        pars = f"{ic[ix]:04}"
        opcode = int(pars[2:]) 
            
        if opcode == 3:
            ic[ic[ix+1]] = comms[id_ix]
            id_ix += 1
            ix += 2
        elif opcode == 4:
            diag_codes.append(ic[ic[ix+1]])
            comms.append(ic[ic[ix+1]])
            ix += 2            
        elif opcode == 99:
            break
            
        else:
            val_1 = ic[ic[ix+1]] if int(pars[1]) == 0 else ic[ix+1]
            val_2 = ic[ic[ix+2]] if int(pars[0]) == 0 else ic[ix+2]
            
            if opcode == 1: 
                ic[ic[ix+3]] = val_1 + val_2
            if opcode == 2:
                ic[ic[ix+3]] = val_1 * val_2
            if opcode == 7:
                ic[ic[ix+3]] = 1 if val_1 < val_2 else 0
            if opcode == 8:
                ic[ic[ix+3]] = 1 if val_1 == val_2 else 0
             
            if opcode == 5:
                ix = val_2 if val_1 != 0 else ix + 3
            elif opcode == 6:
                ix = val_2 if val_1 == 0 else ix + 3
            else:
                ix += 4
        
    return diag_codes

def get_amp_loop_output(ic: np.ndarray, ic_ix: int, comms: typing.List[int], 
                        comms_ix: int) -> typing.Tuple[list, int, bool]:
    '''Returns amp output, index of pause, and whether the opcode '99' 
    was performed. Requires intcode, start index for intcode, list of 
    commands, and what command index to start on'''
    ix = ic_ix
    id_ix = comms_ix
    diag_codes = []
    code_99 = False
    
    while ix < len(ic):
        pars = f"{ic[ix]:04}"
        opcode = int(pars[2:]) 
            
        if opcode == 3:
            ic[ic[ix+1]] = comms[id_ix]
            id_ix += 1
            ix += 2
        elif opcode == 4:
            diag_codes.append(ic[ic[ix+1]])
            ix += 2
            break
        elif opcode == 99:
            code_99 = True
            break
            
        else:
            val_1 = ic[ic[ix+1]] if int(pars[1]) == 0 else ic[ix+1]
            val_2 = ic[ic[ix+2]] if int(pars[0]) == 0 else ic[ix+2]
            
            if opcode == 1: 
                ic[ic[ix+3]] = val_1 + val_2
            if opcode == 2:
                ic[ic[ix+3]] = val_1 * val_2
            if opcode == 7:
                ic[ic[ix+3]] = 1 if val_1 < val_2 else 0
            if opcode == 8:
                ic[ic[ix+3]] = 1 if val_1 == val_2 else 0
             
            if opcode == 5:
                ix = val_2 if val_1 != 0 else ix + 3
            elif opcode == 6:
                ix = val_2 if val_1 == 0 else ix + 3
            else:
                ix += 4
        
    return diag_codes, ix, code_99

def get_complex_fuel(mass: int) -> int:
    '''Returns fuel required for module mass and mass of additional 
    fuel'''
    if mass < 9:
        fuel = 0
    else:
        fuel = get_simple_fuel(mass)
        fuel += get_complex_fuel(fuel)

    return fuel

def get_diagnostic_codes(ic: np.ndarray, sys_id: int = None, off: int = 0) -> list:
    '''Returns diagnostic codes for system ID'''
    ix = 0
    diag_codes = []

    while ix < len(ic):       
        pars = f"{ic[ix]:05}"
        opcode = int(pars[3:])
        
        if opcode == 99:
            break
        
        ic = ic + (ix - len(ic) + 2)*[0] if ix+1 >= len(ic) else ic
        
        par_1 = int(pars[2])
        
        if par_1 == 0:
            par_1_ix = ic[ix+1]
        elif par_1 == 1:
            par_1_ix = ix + 1
        else:
            par_1_ix = off + ic[ix+1]
            
        ic = ic + (par_1_ix - len(ic) + 1)*[0] if par_1_ix >= len(ic) else ic        
            
        if opcode == 3:
            ic[par_1_ix] = sys_id
            ix += 2
        elif opcode == 4:
            diag_codes.append(ic[par_1_ix])
            ix += 2
        elif opcode == 9:
            off += ic[par_1_ix]
            ix += 2
            
        else:
            par_2 = int(pars[1])
            
            if par_2 == 0:
                par_2_ix = ic[ix+2]
            elif par_2 == 1:
                par_2_ix = ix + 2
            else:
                par_2_ix = off + ic[ix+2]
            
            ic = ic + (par_2_ix - len(ic) + 1)*[0] if par_2_ix >= len(ic) else ic        

            if opcode == 5:
                ix = ic[par_2_ix] if ic[par_1_ix] != 0 else ix + 3
            elif opcode == 6:
                ix = ic[par_2_ix] if ic[par_1_ix] == 0 else ix + 3
            
            else:
                par_3 = int(pars[0])
                
                if par_3 == 0:
                    par_3_ix = ic[ix+3]
                elif par_3 == 1:
                    par_3_ix = ix + 3
                else:
                    par_3_ix = off + ic[ix+3]
                
                ic = ic + (par_3_ix - len(ic) + 1)*[0] if par_3_ix >= len(ic) else ic
                
                if opcode == 1: 
                    ic[par_3_ix] = ic[par_1_ix] + ic[par_2_ix]
                if opcode == 2:
                    ic[par_3_ix] = ic[par_1_ix] * ic[par_2_ix]
                if opcode == 7:
                    ic[par_3_ix] = 1 if ic[par_1_ix] < ic[par_2_ix] else 0
                if opcode == 8:
                    ic[par_3_ix] = 1 if ic[par_1_ix] == ic[par_2_ix] else 0
                
                ix += 4
        
    return diag_codes

def get_complex_pwords(lbound: int, hbound: int) -> typing.List[int]:
    '''Returns list of complex passwords'''
    simple_pwords = get_simple_pwords(lbound, hbound)
    complex_pwords = []
    
    for pword in simple_pwords:
        val_count = collections.Counter([int(num) for num in str(pword)])

        if len(val_count.keys()) > 1:
            val_1, val_2 = val_count.most_common(2)
            if val_1[1] > 2 and val_2[1] == 2:
                complex_pwords.append(pword)
            elif val_1[1] <= 2:
                complex_pwords.append(pword)
                
    return complex_pwords

def get_program_code(ic: np.ndarray, state: int) -> typing.Generator:
    '''Returns program code(s) for a given intcode (ic) and desired
    end state. Returned generator will be empty if no codes are found.'''    
    for i, j in itertools.product(range(100), range(100)):
        if state == get_program_state(ic.copy(), i, j):
            code = 100*i + j
            yield code
  
def get_program_state(ic: np.ndarray, noun: int, verb: int) -> int:
    '''Returns program state for a given intcode (ic), noun and verb.
    Noun and verb must be within [0, 99].'''
    ic[1] = noun
    ic[2] = verb
    
    for ix in range(0, len(ic), 4):
        if ic[ix] == 1:
            ic[ic[ix+3]] = ic[ic[ix+1]] + ic[ic[ix+2]] 
        if ic[ix] == 2:
            ic[ic[ix+3]] = ic[ic[ix+1]] * ic[ic[ix+2]]
        if ic[ix] == 99:
            break
 
    return ic[0]

def get_simple_fuel(mass: int) -> int:
    '''Returns initial fuel required for module mass'''
    fuel = max(0, mass // 3 - 2)

    return fuel

def get_simple_pwords(lbound: int, hbound: int) -> typing.List[int]:
    '''Returns list of simple passwords'''
    pwords = []

    for pword in range(lbound, hbound+1):
        split_pword = [int(num) for num in str(pword)]

        n_gram = [(split_pword[ix], split_pword[ix+1]) for ix in range(5)]
        adj_digit = False
        digit_inc = True

        for val_1, val_2 in n_gram:
            if val_2 < val_1:
                digit_inc = False

            if val_1 == val_2:
                adj_digit = True

        if adj_digit and digit_inc:
            pwords.append(pword)

    return pwords

def get_wire_coords(wire: typing.List[str]) -> typing.List[tuple]:
    '''Returns (x, y) coordinates for every sequential position of wire'''
    coords = [(0, 0)]
    
    for move in wire:    
        move_dir = move[0]
        move_lim =  int(move[1:]) + 1
        pcoord = coords[-1]
                
        if move_dir == "U":
            for i in range(1, move_lim):
                coords.append((pcoord[0], pcoord[1]+i))
        elif move_dir == "D":
            for i in range(-1, -move_lim, -1):
                coords.append((pcoord[0], pcoord[1]+i))
        elif move_dir == "R":
            for i in range(1, move_lim):
                coords.append((pcoord[0]+i, pcoord[1]))
        elif move_dir == "L":
            for i in range(-1, -move_lim, -1):
                coords.append((pcoord[0]+i, pcoord[1]))
        
    return coords