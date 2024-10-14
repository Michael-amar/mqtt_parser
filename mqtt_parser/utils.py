def split_byte(num : int):
    """
    split byte to upper and lower nibbles
    """
    upper_bits = num >> 4
    lower_bits = num & 0x0F
    return upper_bits, lower_bits



def update_flag_byte(prev_flag_byte, new_flag_value, start_bit_index, end_bit_index):
    """
    gets the previous flag value, new flag bits to set and their index and returns the updated flag
    LSB is 0 MSB is 7
    """
    
    # Create a mask with 1s in the range of bits to update
    mask = ((1 << (end_bit_index - start_bit_index + 1)) - 1) << start_bit_index

    # Clear the bits in the specified range in the previous flag byte
    cleared_flag_byte = prev_flag_byte & ~mask

    # Set the new flag value in the specified range
    updated_flag_byte = cleared_flag_byte | (new_flag_value << start_bit_index)

    return updated_flag_byte