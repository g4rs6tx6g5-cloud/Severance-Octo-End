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

def calculate_pressure_gauge(long_oi, short_oi):
    """Calculate the Pressure Gauge: (Long OI - Short OI) / Total OI"""
    total_oi = long_oi + short_oi
    if total_oi == 0:
        return 0
    return (long_oi - short_oi) / total_oi

def calculate_trend_status(current_price, ma50):
    """Determine trend status based on MA50"""
    if current_price > ma50:
        return "BULLISH (AETOS ACTIVE)", "🟢"
    else:
        return "BEARISH (KHRUSOS ACTIVE)", "🔴"

def main():
    # Configure Streamlit page
    st.set_page_config(
        page_title="Tri-Framework Oracle - Trading Mastery",
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
    .pressure-high-container {
        background-color: #dc2626;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #ef4444;
    }
    .pressure-low-container {
        background-color: #16a34a;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #22c55e;
    }
    .neutral-container {
        background-color: #f59e0b;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #fbbf24;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # App title
    st.title("🔮 Tri-Framework Oracle - Trading Mastery")
    st.markdown("*Mathematical precision for BTC/USDT trading mastery*")
    
    # Navigation
    tab1, tab2, tab3 = st.tabs(["Arbitrage Calculator", "Pressure Gauge", "Market Analysis"])
    
    with tab1:
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
        if st.button("🔮 Calculate Arbitrage", type="secondary"):
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
    
    with tab2:
        st.header("📊 Pressure Gauge Protocol")
        st.markdown("*Positioning analysis: (Long OI - Short OI) / Total OI*")
        
        col1, col2 = st.columns(2)
        
        with col1:
            long_oi = st.number_input(
                "Long Open Interest (BTC):",
                min_value=0.0,
                value=5500000.0,
                step=100000.0,
                format="%.0f",
                key="long_oi"
            )
        
        with col2:
            short_oi = st.number_input(
                "Short Open Interest (BTC):",
                min_value=0.0,
                value=4500000.0,
                step=100000.0,
                format="%.0f",
                key="short_oi"
            )
        
        if st.button("📈 Calculate Pressure Gauge", type="secondary"):
            with st.spinner("Analyzing positioning..."):
                pressure_gauge = calculate_pressure_gauge(long_oi, short_oi)
                
                st.markdown("### 📊 Positioning Analysis:")
                
                # Display raw data
                st.metric("Total Open Interest", f"{long_oi + short_oi:,.0f} BTC")
                st.metric("Long OI", f"{long_oi:,.0f} BTC")
                st.metric("Short OI", f"{short_oi:,.0f} BTC")
                
                # Display pressure gauge
                st.markdown(f"### 🎯 Pressure Gauge: {pressure_gauge:.3f}")
                
                # Interpretation
                if pressure_gauge > 0.5:
                    st.markdown(
                        f'<div class="pressure-high-container"><h4>🔴 EXTREME LONGS ({pressure_gauge:.1%})</h4><p>Potential for bearish squeeze if market breaks down</p></div>',
                        unsafe_allow_html=True
                    )
                elif pressure_gauge < -0.5:
                    st.markdown(
                        f'<div class="pressure-low-container"><h4>🟢 EXTREME SHORTS ({abs(pressure_gauge):.1%})</h4><p>Potential for bullish squeeze if market breaks up</p></div>',
                        unsafe_allow_html=True
                    )
                elif pressure_gauge > 0.2:
                    st.markdown(
                        f'<div class="pressure-high-container"><h4>🟡 HIGH LONGS ({pressure_gauge:.1%})</h4><p>Caution - longs may be crowded</p></div>',
                        unsafe_allow_html=True
                    )
                elif pressure_gauge < -0.2:
                    st.markdown(
                        f'<div class="pressure-low-container"><h4>🟡 HIGH SHORTS ({abs(pressure_gauge):.1%})</h4><p>Caution - shorts may be crowded</p></div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div class="neutral-container"><h4>⚪️ BALANCED ({pressure_gauge:.1%})</h4><p>Positioning appears neutral</p></div>',
                        unsafe_allow_html=True
                    )
                
                # Analysis interpretation
                st.markdown("### 🔍 Analysis:")
                if pressure_gauge > 0.7:
                    st.warning("⚠️ EXTREME LONG CONGESTION - Potential for bearish break if support fails")
                elif pressure_gauge < -0.7:
                    st.success("✅ EXTREME SHORT CONGESTION - Potential for bullish break if resistance breaks")
                elif abs(pressure_gauge) > 0.3:
                    st.info(f"ℹ️ POSITIONING ASYMMETRY DETECTED - Current bias: {'LONG' if pressure_gauge > 0 else 'SHORT'}")
    
    with tab3:
        st.header("📈 Market Analysis Dashboard")
        st.markdown("*Tri-Framework integration*")
        
        col1, col2 = st.columns(2)
        
        with col1:
            current_price = st.number_input(
                "Current BTC/USDT Price:",
                min_value=0.0,
                value=109550.0,
                step=100.0,
                format="%.2f",
                key="current_price"
            )
            
            ma50 = st.number_input(
                "MA50 Value:",
                min_value=0.0,
                value=109400.0,
                step=100.0,
                format="%.2f",
                key="ma50"
            )
        
        with col2:
            support_level = st.number_input(
                "Critical Support Level:",
                min_value=0.0,
                value=109400.0,
                step=100.0,
                format="%.2f",
                key="support"
            )
            
            resistance_level = st.number_input(
                "Critical Resistance Level:",
                min_value=0.0,
                value=109715.0,
                step=100.0,
                format="%.2f",
                key="resistance"
            )
        
        if st.button("🎯 Analyze Market Structure", type="secondary"):
            with st.spinner("Analyzing market structure..."):
                # Trend analysis
                trend_status, trend_emoji = calculate_trend_status(current_price, ma50)
                
                st.markdown("### 📊 Market Structure Analysis:")
                
                # Display current market status
                st.metric("Current Price", f"${current_price:,.2f}")
                st.metric("MA50", f"${ma50:,.2f}")
                st.metric("Support Level", f"${support_level:,.2f}")
                st.metric("Resistance Level", f"${resistance_level:,.2f}")
                
                # Trend analysis
                st.markdown(f"### 🎯 Trend Status: {trend_emoji} {trend_status}")
                
                # Price position relative to levels
                st.markdown("### 📍 Price Positioning:")
                if current_price > resistance_level:
                    st.success(f"✅ PRICE ABOVE RESISTANCE: {current_price - resistance_level:.2f} above")
                elif current_price < support_level:
                    st.error(f"❌ PRICE BELOW SUPPORT: {support_level - current_price:.2f} below")
                else:
                    st.info(f"⚠️ PRICE IN RANGE: {current_price - support_level:.2f} from support, {resistance_level - current_price:.2f} from resistance")
                
                # Framework integration
                st.markdown("### 🔮 Tri-Framework Status:")
                if current_price > ma50:
                    st.success("✅ AETOS PROTOCOL ACTIVE - Trading with primary trend")
                    st.info("🎯 Strategy: Look for entries above resistance levels")
                else:
                    st.warning("⚠️ KHRUSOS PROTOCOL ACTIVE - Capital preservation mode")
                    st.info("🎯 Strategy: Look for entries below support levels")
                
                # Compression analysis
                compression_distance = resistance_level - support_level
                if compression_distance < 1000:  # Less than $1000 range
                    st.warning(f"⚠️ COMPRESSION DETECTED: Only {compression_distance:.2f} points between support and resistance")
                    st.info("🎯 ALPHA COMPRESSION SPRING - High probability setup when compression breaks")
                else:
                    st.info(f"📊 Current Range: {compression_distance:.2f} points")
    
    # Information section
    with st.expander("📚 Framework Information"):
        st.markdown("""
        **TRI-FRAMEWORK OVERVIEW:**
        
        1. **TREND (AETOS PROTOCOL)**: Price > MA50 for bullish, else bearish
        2. **POSITIONING (PRESSURE GAUGE)**: (Long OI - Short OI) / Total OI
        3. **EXECUTION**: Monitor funding rates and market structure
        
        **PRESSURE GAUGE INTERPRETATION:**
        - > 0.7: EXTREME LONGS (potential bearish squeeze)
        - < -0.7: EXTREME SHORTS (potential bullish squeeze)  
        - 0.2 to 0.7: HIGH LONGS (caution)
        - -0.7 to -0.2: HIGH SHORTS (caution)
        - -0.2 to 0.2: BALANCED positioning
        
        **ALPHA COMPRESSION SPRING:**
        When price compresses in tight range with extreme positioning, 
        a break often triggers a squeeze in the opposite direction.
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("*For personal learning and trading education only*")
    st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

if __name__ == "__main__":
    main()
