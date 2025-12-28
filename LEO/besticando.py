import math
import numpy as np
from scipy.special import zeta
import matplotlib.pyplot as plt

class RiemannZeroCalculator:
    def __init__(self):
        # Scientifically accurate non-trivial zeros (imaginary parts)
        # First 15 non-trivial zeros of Riemann Zeta function
        self.known_zeros = [
            14.134725141734693790,
            21.022039638771554993,
            25.010857580145688763,
            30.424876125859513210,
            32.935061587739189690,
            37.586178158825671257,
            40.918719012147495187,
            43.327073280914999519,
            48.005150881167159727,
            49.773832477672302181,
            52.970321477714460644,
            56.446247697063394804,
            59.347044002602353079,
            60.831778524609809844,
            65.112544048081606660
        ]
        
        # Precision for calculations
        self.precision = 1e-12
        self.max_iterations = 1000
    
    def gamma_function(self, gamma_n):
        """Calculate γₙ₊₁ = γₙ + 2π * log(γₙ + 1) / (logγₙ)²"""
        if gamma_n <= 1:
            return gamma_n + 0.1  # Prevent division by zero or negative logs
        
        log_gamma = math.log(gamma_n)
        if abs(log_gamma) < self.precision:
            return gamma_n + 0.1
            
        numerator = 2 * math.pi * math.log(gamma_n + 1)
        denominator = log_gamma ** 2
        
        if abs(denominator) < self.precision:
            return gamma_n + 0.1
            
        return gamma_n + numerator / denominator
    
    def riemann_zeta_at_zero(self, t):
        """Calculate Riemann Zeta function at 1/2 + it"""
        # Using approximation for critical line
        real_part = 0.5
        return zeta(complex(real_part, t))
    
    def calculate_sequence(self, start_value=None):
        """Calculate the sequence using both formulas"""
        if start_value is None:
            start_value = self.known_zeros[0]
        
        results = []
        gamma_current = start_value
        previous_zeta = None
        previous_gamma = None
        spawn_counter = 0
        total_zeros_counted = 0
        
        print(f"{'Entry':<6} {'Known Zero':<18} {'Zeta Output':<15} {'New Formula':<15} "
              f"{'Disparity':<12} {'Zeta Increase':<15} {'Gamma Increase':<15} "
              f"{'Spawn Counter':<14} {'Total Zeros':<12}")
        print("-" * 130)
        
        for i, known_zero in enumerate(self.known_zeros):
            # Calculate Riemann Zeta output
            zeta_output_complex = self.riemann_zeta_at_zero(known_zero)
            zeta_output = abs(zeta_output_complex)  # Magnitude for comparison
            
            # Calculate new formula output
            gamma_output = gamma_current
            
            # Calculate disparities and increases
            disparity = abs(zeta_output - gamma_output)
            
            zeta_increase = abs(zeta_output - previous_zeta) if previous_zeta is not None else 0
            gamma_increase = abs(gamma_output - previous_gamma) if previous_gamma is not None else 0
            
            # Check if new formula spawned a zero (when it's close to a known zero)
            zero_threshold = 0.1
            if abs(gamma_output - known_zero) < zero_threshold:
                spawn_counter += 1
                total_zeros_counted += 1
            
            total_zeros_counted += 1
            
            # Store results
            result = {
                'entry': i + 1,
                'known_zero': known_zero,
                'zeta_output': zeta_output,
                'gamma_output': gamma_output,
                'disparity': disparity,
                'zeta_increase': zeta_increase,
                'gamma_increase': gamma_increase,
                'spawn_counter': spawn_counter,
                'total_zeros': total_zeros_counted
            }
            results.append(result)
            
            # Print current result
            print(f"{i+1:<6} {known_zero:<18.6f} {zeta_output:<15.6e} {gamma_output:<15.6f} "
                  f"{disparity:<12.6e} {zeta_increase:<15.6e} {gamma_increase:<15.6f} "
                  f"{spawn_counter:<14} {total_zeros_counted:<12}")
            
            # Update for next iteration
            previous_zeta = zeta_output
            previous_gamma = gamma_output
            gamma_current = self.gamma_function(gamma_current)
        
        return results
    
    def analyze_convergence(self, results):
        """Analyze the convergence behavior"""
        print("\n" + "="*60)
        print("CONVERGENCE ANALYSIS")
        print("="*60)
        
        disparities = [r['disparity'] for r in results]
        avg_disparity = np.mean(disparities)
        max_disparity = np.max(disparities)
        min_disparity = np.min(disparities)
        
        print(f"Average Disparity: {avg_disparity:.6e}")
        print(f"Maximum Disparity: {max_disparity:.6e}")
        print(f"Minimum Disparity: {min_disparity:.6e}")
        print(f"Total Zeros Spawned by New Formula: {results[-1]['spawn_counter']}")
        print(f"Final Total Zeros Counted: {results[-1]['total_zeros']}")
        
        # Calculate correlation between sequences
        zeta_values = [r['zeta_output'] for r in results]
        gamma_values = [r['gamma_output'] for r in results]
        
        if len(zeta_values) > 1:
            correlation = np.corrcoef(zeta_values, gamma_values)[0,1]
            print(f"Correlation between sequences: {correlation:.6f}")
    
    def plot_comparison(self, results):
        """Plot the comparison between Riemann Zeta and the new formula"""
        entries = [r['entry'] for r in results]
        zeta_vals = [r['zeta_output'] for r in results]
        gamma_vals = [r['gamma_output'] for r in results]
        disparities = [r['disparity'] for r in results]
        
        plt.figure(figsize=(15, 10))
        
        # Plot 1: Values comparison
        plt.subplot(2, 2, 1)
        plt.plot(entries, zeta_vals, 'b-', label='Riemann Zeta Output', linewidth=2)
        plt.plot(entries, gamma_vals, 'r--', label='New Formula Output', linewidth=2)
        plt.xlabel('Entry Number')
        plt.ylabel('Output Value')
        plt.title('Comparison: Riemann Zeta vs New Formula')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot 2: Disparities
        plt.subplot(2, 2, 2)
        plt.semilogy(entries, disparities, 'g-', linewidth=2)
        plt.xlabel('Entry Number')
        plt.ylabel('Disparity (log scale)')
        plt.title('Disparity Between Formulas')
        plt.grid(True, alpha=0.3)
        
        # Plot 3: Increases
        plt.subplot(2, 2, 3)
        zeta_increases = [r['zeta_increase'] for r in results if r['zeta_increase'] > 0]
        gamma_increases = [r['gamma_increase'] for r in results if r['gamma_increase'] > 0]
        
        # Use appropriate indices for plotting
        zeta_indices = entries[1:len(zeta_increases)+1]
        gamma_indices = entries[1:len(gamma_increases)+1]
        
        if zeta_indices and zeta_increases:
            plt.plot(zeta_indices, zeta_increases, 'b-', label='Zeta Increase', linewidth=2)
        if gamma_indices and gamma_increases:
            plt.plot(gamma_indices, gamma_increases, 'r-', label='Gamma Increase', linewidth=2)
        
        plt.xlabel('Entry Number')
        plt.ylabel('Increase from Previous')
        plt.title('Formula Increases Over Sequence')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot 4: Spawn counter progression
        plt.subplot(2, 2, 4)
        spawn_counts = [r['spawn_counter'] for r in results]
        plt.plot(entries, spawn_counts, 'purple', linewidth=2)
        plt.xlabel('Entry Number')
        plt.ylabel('Spawn Counter')
        plt.title('New Formula Zero Spawn Progression')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

def main():
    calculator = RiemannZeroCalculator()
    
    print("RIEMANN ZETA FUNCTION vs NEW GAMMA FORMULA ANALYSIS")
    print("=" * 130)
    print(f"Using {len(calculator.known_zeros)} scientifically accurate non-trivial zeros")
    print(f"Precision: {calculator.precision}")
    print()
    
    # Calculate the sequence
    results = calculator.calculate_sequence()
    
    # Perform convergence analysis
    calculator.analyze_convergence(results)
    
    # Plot results
    calculator.plot_comparison(results)
    
    # Additional detailed output
    print("\n" + "="*60)
    print("DETAILED ZERO ANALYSIS")
    print("="*60)
    
    for i, result in enumerate(results[:5]):  # Show first 5 for brevity
        print(f"Zero {i+1}:")
        print(f"  Known Value: {result['known_zero']:.12f}")
        print(f"  |ζ(1/2 + it)|: {result['zeta_output']:.6e}")
        print(f"  Gamma Formula: {result['gamma_output']:.12f}")
        print(f"  Disparity: {result['disparity']:.6e}")
        print()

if __name__ == "__main__":
    main()