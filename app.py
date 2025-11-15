import streamlit as st
import math
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_implied_probability(decimal_odds):
    """Calculate implied probability from decimal odds"""
    if decimal_odds <= 0:
        return 0
    return 1 / decimal_odds

def calculate_total_implied_probability(implied_probs):
    """Calculate total implied probability"""
    return sum(implied_probs)

def calculate_stakes(bankroll, implied_probs, total_implied):
    """Calculate stakes for each outcome"""
    stakes = []
    for prob in implied_probs:
        stake = (bankroll * prob) / total_implied
        stakes.append(stake)
    return stakes

def calculate_profit(stake, odds):
    """Calculate profit from a single bet"""
    return (stake * odds) - sum([s for s in calculate_stakes(stake, [1/odds], 1/odds)])

def validate_positive_number(value):
    """Validate that input is a positive number"""
    return value and value > 0

def process_arbitrage_calculation(odds_list, bankroll):
    """Process the complete arbitrage calculation"""
    try:
        # Log calculation attempt
        logger.info(f"Calculation attempt: odds={odds_list}, bankroll={bankroll}")
        
        # Calculate implied probabilities
        implied_probs = [calculate_implied_probability(odd) for odd in odds_list]
        
        # Calculate total implied probability
        total_implied = calculate_total_implied_probability(implied_probs)
        
        # Check for arbitrage
        is_arb_found = total_implied < 1.0
        
        if is_arb_found:
            # Calculate stakes
            stakes = calculate_stakes(bankroll, implied_probs, total_implied)
            
            # Calculate profit (same for all outcomes in valid arb)
            profit = (stakes[0] * odds_list[0]) - bankroll
            
            return {
                'is_arb_found': True,
                'stakes': stakes,
                'profit': profit,
                'total_implied': total_implied,
                'implied_probs': implied_probs,
                'error': None
            }
        else:
            return {
                'is_arb_found': False,
                'stakes': [],
                'profit': 0,
                'total_implied': total_implied,
                'implied_probs': implied_probs,
                'error': None
            }
    except Exception as e:
        logger.error(f"Calculation error: {str(e)}")
        return {
            'is_arb_found': False,
            'stakes': [],
            'profit': 0,
            'total_implied': 0,
            'implied_probs': [],
            'error': str(e)
        }

def main():
    # Configure Streamlit page
    st.set_page_config(
        page_title="Arbitrage Oracle - Personal Learning Tool",
        page_icon="🔮",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for dark mode and styling
    st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stTextInput > div > div > input {
        background-color: #202938;
        color: #ffffff;
        border: 1px solid #374151;
    }
    .stNumberInput > div > div > input {
        background-color: #202938;
        color: #ffffff;
        border: 1px solid #374151;
    }
    .stButton > button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #1d4ed8;
    }
    .metric-container {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #2563eb;
    }
    .success-container {
        background-color: #166534;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #22c55e;
    }
    .error-container {
        background-color: #991b1b;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #ef4444;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # App title
    st.title("🔮 Arbitrage Oracle - Personal Learning Tool")
    st.markdown("*Mathematical precision for personal trading education*")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        num_outcomes = st.radio(
            "Number of Outcomes:",
            options=[2, 3],
            index=0,
            horizontal=True
        )
        
        st.markdown("---")
        st.markdown("**Example Setup:**")
        st.markdown("- Odds: 2.0, 3.0, 4.0")
        st.markdown("- Bankroll: £100")
        st.markdown("- Expected: Arbitrage found!")
        
        st.markdown("---")
        st.markdown("*Personal Learning Tool*")
        st.markdown("For educational purposes only")
    
    # Main input area
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # Get odds inputs based on selection
    odds_inputs = []
    
    with col1:
        odd1 = st.number_input(
            "Outcome A Odds:",
            min_value=0.01,
            max_value=100.0,
            value=2.0,
            step=0.01,
            format="%.2f",
            key="odd1"
        )
        odds_inputs.append(odd1)
    
    with col2:
        odd2 = st.number_input(
            "Outcome B Odds:",
            min_value=0.01,
            max_value=100.0,
            value=3.0,
            step=0.01,
            format="%.2f",
            key="odd2"
        )
        odds_inputs.append(odd2)
    
    if num_outcomes == 3:
        with col3:
            odd3 = st.number_input(
                "Outcome C Odds:",
                min_value=0.01,
                max_value=100.0,
                value=4.0,
                step=0.01,
                format="%.2f",
                key="odd3"
            )
            odds_inputs.append(odd3)
    else:
        odds_inputs.append(None)  # Placeholder for 2-outcome case
    
    # Remove None values for 2-outcome case
    if num_outcomes == 2:
        odds_inputs = [odd for odd in odds_inputs if odd is not None]
    
    # Bankroll input
    bankroll = st.number_input(
        "Total Bankroll (£):",
        min_value=0.01,
        value=100.0,
        step=1.0,
        format="%.2f",
        key="bankroll"
    )
    
    # Calculate button
    if st.button("🔮 Calculate Arbitrage", type="primary"):
        with st.spinner("Processing mathematical calculations..."):
            result = process_arbitrage_calculation(odds_inputs, bankroll)
            
            if result['error']:
                st.markdown(
                    f'<div class="error-container"><strong>Error:</strong> {result["error"]}</div>',
                    unsafe_allow_html=True
                )
            else:
                # Display results
                if result['is_arb_found']:
                    st.markdown(
                        '<div class="success-container"><h3>✅ ARBITRAGE OPPORTUNITY FOUND!</h3></div>',
                        unsafe_allow_html=True
                    )
                    
                    st.markdown("### 📊 Results:")
                    
                    # Display implied probabilities
                    st.markdown("#### Implied Probabilities:")
                    prob_cols = st.columns(len(odds_inputs))
                    for i, (odd, prob) in enumerate(zip(odds_inputs, result['implied_probs'])):
                        with prob_cols[i]:
                            st.metric(
                                label=f"Outcome {chr(65+i)}",
                                value=f"{prob:.2%}",
                                delta=f"Odds: {odd}"
                            )
                    
                    # Display total implied probability
                    st.markdown(f"**Total Implied Probability:** {result['total_implied']:.2%}")
                    st.markdown(f"**Market Efficiency:** {(1 - result['total_implied']):.2%} potential profit")
                    
                    # Display stakes and profit
                    st.markdown("#### Recommended Stakes:")
                    stake_cols = st.columns(len(odds_inputs))
                    for i, (stake, odd) in enumerate(zip(result['stakes'], odds_inputs)):
                        with stake_cols[i]:
                            st.metric(
                                label=f"Stake on {chr(65+i)}",
                                value=f"£{stake:.2f}",
                                delta=f"Odds: {odd}"
                            )
                    
                    st.markdown(
                        f"### 💰 Guaranteed Profit: £{result['profit']:.2f} ({(result['profit']/bankroll)*100:.2f}%)"
                    )
                    
                else:
                    st.markdown(
                        f'<div class="error-container"><h3>❌ NO ARBITRAGE FOUND</h3><p>Total Implied Probability: {result["total_implied"]:.2%}</p></div>',
                        unsafe_allow_html=True
                    )
                    
                    # Show why no arb exists
                    if result['total_implied'] > 1.0:
                        inefficiency = (result['total_implied'] - 1.0) * 100
                        st.info(f"This market has {inefficiency:.2f}% overround - bookmaker's edge")
    
    # Information section
    with st.expander("📚 How Arbitrage Works"):
        st.markdown("""
        **Arbitrage** occurs when you can place bets on all possible outcomes of an event 
        and guarantee a profit regardless of the result.
        
        **Mathematical Principle:**
        - Calculate implied probability for each outcome: 1 / decimal odds
        - If total implied probability < 100%, arbitrage exists
        - Stake calculation ensures equal profit across all outcomes
        
        **Formula:**
        ```
        Stake on Outcome A = (Total Bankroll × Implied Probability of Other Outcomes) / Total Implied Probability
        ```
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("*For personal learning and mathematical exploration only*")
    st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

if __name__ == "__main__":
    main()
