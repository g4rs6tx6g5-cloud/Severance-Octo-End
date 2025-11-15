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

def calculate_fibonacci_levels(high, low):
    """Calculate Fibonacci retracement levels"""
    diff = high - low
    levels = {
        '23.6%': high - (diff * 0.236),
        '38.2%': high - (diff * 0.382),
        '50.0%': high - (diff * 0.500),
        '61.8%': high - (diff * 0.618),
        '78.6%': high - (diff * 0.786),
        'support': low,
        'resistance': high
    }
    return levels

def calculate_timeframe_multiplier(timeframe):
    """Calculate multiplier for different timeframes"""
    multipliers = {
        '1m': 1,
        '5m': 5,
        '15m': 15,
        '30m': 30,
        '1h': 60,
        '4h': 240,
        '1d': 1440,
        '1w': 10080
    }
    return multipliers.get(timeframe, 60)

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
    .stSelectbox > div > div {
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
    .fib-level {
        background-color: #1f2937;
        padding: 8px;
        border-radius: 5px;
        margin: 2px 0;
        border-left: 2px solid #8b5cf6;
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
    tab1, tab2, tab3, tab4 = st.tabs(["Arbitrage Calculator", "Pressure Gauge", "Market Analysis", "Fibonacci Engine"])
    
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
        st.markdown("*Tri-Framework integration with Fibonacci alignment*")
        
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
            recent_high = st.number_input(
                "Recent Swing High:",
                min_value=0.0,
                value=110000.0,
                step=100.0,
                format="%.2f",
                key="recent_high"
            )
            
            recent_low = st.number_input(
                "Recent Swing Low:",
                min_value=0.0,
                value=109000.0,
                step=100.0,
                format="%.2f",
                key="recent_low"
            )
        
        if st.button("🎯 Analyze Market Structure", type="secondary"):
            with st.spinner("Analyzing market structure..."):
                # Calculate Fibonacci levels
                fib_levels = calculate_fibonacci_levels(recent_high, recent_low)
                
                # Trend analysis
                trend_status, trend_emoji = calculate_trend_status(current_price, ma50)
                
                st.markdown("### 📊 Market Structure Analysis:")
                
                # Display current market status
                st.metric("Current Price", f"${current_price:,.2f}")
                st.metric("MA50", f"${ma50:,.2f}")
                st.metric("Swing High", f"${recent_high:,.2f}")
                st.metric("Swing Low", f"${recent_low:,.2f}")
                
                # Trend analysis
                st.markdown(f"### 🎯 Trend Status: {trend_emoji} {trend_status}")
                
                # Fibonacci levels
                st.markdown("### 📐 Fibonacci Levels:")
                for level_name, level_value in fib_levels.items():
                    if level_name not in ['support', 'resistance']:
                        color = "🟢" if abs(current_price - level_value) < 1000 else "⚪️"
                        st.markdown(f"<div class='fib-level'>{color} **{level_name}: ${level_value:,.2f}**</div>", unsafe_allow_html=True)
                
                # Price position relative to Fibonacci levels
                st.markdown("### 📍 Price Positioning:")
                closest_fib = min(fib_levels.values(), key=lambda x: abs(x - current_price))
                fib_distance = abs(current_price - closest_fib)
                st.info(f"Closest Fibonacci level: ${closest_fib:,.2f} (Distance: ${fib_distance:,.2f})")
                
                # Framework integration
                st.markdown("### 🔮 Tri-Framework Status:")
                if current_price > ma50:
                    st.success("✅ AETOS PROTOCOL ACTIVE - Trading with primary trend")
                    st.info("🎯 Strategy: Look for entries above key Fibonacci levels")
                else:
                    st.warning("⚠️ KHRUSOS PROTOCOL ACTIVE - Capital preservation mode")
                    st.info("🎯 Strategy: Look for entries below key Fibonacci levels")
                
                # Compression analysis
                compression_distance = recent_high - recent_low
                if compression_distance < 1000:  # Less than $1000 range
                    st.warning(f"⚠️ COMPRESSION DETECTED: Only {compression_distance:.2f} points between swing high and low")
                    st.info("🎯 ALPHA COMPRESSION SPRING - High probability setup when compression breaks")
                else:
                    st.info(f"📊 Current Range: {compression_distance:.2f} points")
    
    with tab4:
        st.header("🧮 Fibonacci Engine - Multi-Timeframe Analysis")
        st.markdown("*Magnifying glass for small timeframes, binoculars for long-term trends*")
        
        col1, col2 = st.columns(2)
        
        with col1:
            high_price = st.number_input(
                "Swing High Price:",
                min_value=0.0,
                value=110000.0,
                step=100.0,
                format="%.2f",
                key="high_price"
            )
            
            low_price = st.number_input(
                "Swing Low Price:",
                min_value=0.0,
                value=109000.0,
                step=100.0,
                format="%.2f",
                key="low_price"
            )
        
        with col2:
            current_price_fib = st.number_input(
                "Current Price:",
                min_value=0.0,
                value=109550.0,
                step=100.0,
                format="%.2f",
                key="current_price_fib"
            )
            
            timeframe = st.selectbox(
                "Analysis Timeframe:",
                options=['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w'],
                index=4,  # Default to 1h
                key="timeframe"
            )
        
        if st.button("🧮 Calculate Fibonacci Analysis", type="secondary"):
            with st.spinner("Calculating Fibonacci levels..."):
                # Calculate Fibonacci levels
                fib_levels = calculate_fibonacci_levels(high_price, low_price)
                
                st.markdown("### 📐 Fibonacci Retracement Levels:")
                
                # Create columns for Fibonacci levels
                cols = st.columns(5)
                fib_items = list(fib_levels.items())
                
                for i, (level_name, level_value) in enumerate(fib_levels.items()):
                    if level_name not in ['support', 'resistance']:
                        with cols[i % 5]:
                            st.metric(label=level_name, value=f"${level_value:,.2f}")
                
                st.markdown("### 📍 Current Price Analysis:")
                
                # Determine which Fibonacci level current price is closest to
                distances = {name: abs(current_price_fib - value) for name, value in fib_levels.items()}
                closest_level = min(distances, key=distances.get)
                closest_distance = distances[closest_level]
                
                st.metric(
                    label=f"Closest Level: {closest_level}",
                    value=f"${fib_levels[closest_level]:,.2f}",
                    delta=f"${closest_distance:.2f} away"
                )
                
                # Fibonacci level interpretation
                st.markdown("### 🎯 Fibonacci Interpretation:")
                
                # Check if price is near specific levels
                for level_name, level_value in fib_levels.items():
                    if level_name not in ['support', 'resistance']:
                        distance = abs(current_price_fib - level_value)
                        if distance < 500:  # If within $500 of level
                            st.success(f"🎯 PRICE NEAR {level_name} LEVEL (${level_value:,.2f}) - Potential Support/Resistance")
                        elif distance < 1000:  # If within $1000 of level
                            st.info(f"ℹ️ PRICE APPROACHING {level_name} LEVEL (${level_value:,.2f})")
                
                # Timeframe analysis
                st.markdown(f"### 🕐 Timeframe Analysis: {timeframe}")
                multiplier = calculate_timeframe_multiplier(timeframe)
                st.info(f"Timeframe multiplier: {multiplier} minutes")
                
                if multiplier <= 60:  # Short timeframes (1m-1h)
                    st.warning("🔍 MAGNIFYING GLASS MODE: Short-term analysis, higher volatility expected")
                elif multiplier <= 1440:  # Medium timeframes (4h-1d)
                    st.info("⚖️ BALANCED VIEW: Medium-term analysis, balanced risk/reward")
                else:  # Long timeframes (1d-1w)
                    st.success(" binoculars MODE: Long-term analysis, lower volatility expected")
                
                # Multi-timeframe alignment
                st.markdown("### 🎯 Multi-Timeframe Alignment:")
                if current_price_fib > fib_levels['50.0%']:
                    st.success("📈 PRICE ABOVE 50% LEVEL - Bullish bias on multiple timeframes")
                else:
                    st.error("📉 PRICE BELOW 50% LEVEL - Bearish bias on multiple timeframes")
                
                if abs(current_price_fib - fib_levels['38.2%']) < 500 or abs(current_price_fib - fib_levels['61.8%']) < 500:
                    st.warning("⚠️ PRICE NEAR KEY FIBONACCI LEVEL - High probability reversal zone")
    
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
        
        **FIBONACCI LEVELS:**
        - 23.6%, 38.2%, 50%, 61.8%, 78.6% - Key support/resistance levels
        - Price often reverses at these levels
        - Multi-timeframe alignment increases probability
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("*For personal learning and trading education only*")
    st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

if __name__ == "__main__":
    main()