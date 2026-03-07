def booth_multiplier(multiplicand, multiplier, bits=8):
    # 1. Initialize Registers
    # A: Accumulator, Q: Multiplier, Q_prev: extra bit (Qn+1)
    a = 0
    q = multiplier & ((1 << bits) - 1)  # Ensure n-bit representation
    m = multiplicand & ((1 << bits) - 1)
    q_prev = 0
    
    # Mask to keep numbers within the specified bit length
    mask = (1 << bits) - 1

    for _ in range(bits):
        # 2. Check the last bit of Q and the previous bit (Q_prev)
        last_bit_q = q & 1
        
        # 3. Apply the Decision Logic
        if last_bit_q == 1 and q_prev == 0:
            a = (a - m) & mask
        elif last_bit_q == 0 and q_prev == 1:
            a = (a + m) & mask
        
        # 4. Arithmetic Right Shift (ASR)
        # Combined A and Q shift: [A][Q][Q_prev]
        combined = (a << (bits + 1)) | (q << 1) | q_prev
        
        # Preserve the sign bit for ASR
        sign_bit = combined & (1 << (2 * bits))
        combined >>= 1
        if sign_bit:
            combined |= (1 << (2 * bits))
            
        # Update registers from the shifted combined value
        q_prev = combined & 1
        q = (combined >> 1) & mask
        a = (combined >> (bits + 1)) & mask

    # Combine A and Q for the final result
    result_raw = (a << bits) | q
    
    # Handle two's complement for the final signed integer output
    if result_raw & (1 << (2 * bits - 1)):
        return result_raw - (1 << (2 * bits))
    return result_raw

# Example usage: 7 * -3
print(f"Result: {booth_multiplier(7, -3)}")  # Output: -21
