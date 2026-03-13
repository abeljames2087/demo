import pandas as pd
import ollama
import os

def main():
    print("📊 SUPPLY CHAIN FINANCIAL IMPACT ANALYST (Gemma 3)")
    print("--------------------------------------------------")

    # 1. LOAD THE CSV FILE
    file_path = "D.csv"
    
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found! Please ensure it's in the same folder.")
        # Alternatively, create a mock one if it doesn't exist for testing:
        print("Creating a temporary mock 'D.csv' for demonstration purposes...")
        mock_data = {
            'event_id': ['EVT-001', 'EVT-002', 'EVT-003'],
            'event_type': ['Port Strike', 'Typhoon', 'Congestion'],
            'affected_port': ['Port of LA', 'South China Sea', 'Singapore'],
            'status': ['Critical', 'High', 'Medium'],
            'estimated_delay_days': [5, 3, 2],
            'value_at_risk': [1500000, 2400000, 800000]
        }
        pd.DataFrame(mock_data).to_csv(file_path, index=False)
        print("Created mock D.csv.")
        
    df = pd.read_csv(file_path)

    # 2. THE INPUTS
    target_port = input("📍 Enter the Port to analyze: ").strip()

    # 3. FILTERING
    # This checks the 'affected_port' column for the target port
    matches = df[df['affected_port'].str.contains(target_port, case=False, na=False)]

    # 4. DATA OUTPUT & CALCULATION
    print("\n--- 📈 FINANCIAL & LOGISTICAL IMPACT ---")
    if not matches.empty:
        total_delay = matches['estimated_delay_days'].sum() if 'estimated_delay_days' in matches.columns else "Unknown"
        total_risk = matches['value_at_risk'].sum() if 'value_at_risk' in matches.columns else "Unknown"
        
        print(f"Found {len(matches)} active disruption(s) affecting {target_port}:\n")
        # Displaying the raw data matches
        columns_to_show = ['event_id', 'event_type', 'status']
        if 'estimated_delay_days' in matches.columns: columns_to_show.append('estimated_delay_days')
        if 'value_at_risk' in matches.columns: columns_to_show.append('value_at_risk')
            
        print(matches[columns_to_show].to_string(index=False))
        print(f"\n>> Total Estimated Delay: {total_delay} Days")
        
        if isinstance(total_risk, (int, float)):
            print(f">> Total Value at Risk: ${total_risk:,.2f}")
        else:
             print(f">> Total Value at Risk: {total_risk}")

    else:
        print(f"✅ No immediate disruptions found in {file_path} for {target_port}.")

    print("---------------------------------------")

    # 5. AI ANALYSIS (Using Gemma 3)
    print("\n🤖 AI ANALYSIS (gemma3:4b):")
    
    if not matches.empty:
        data_text = matches.to_string(index=False)
        prompt = f"""
        You are the Supply Chain Financial Analyst Agent.
        Review the following disruption data for {target_port}:
        
        {data_text}
        
        Summarize the financial and logistical impact of these disruptions in a professional 3-sentence report. 
        Focus on the 'value_at_risk' and 'estimated_delay_days' if they are present.
        """
    else:
        prompt = f"You are a Supply Chain Analyst. Based on current data, {target_port} is operating normally with no delays. Provide a brief 1-sentence confirmation."

    try:
        # Calling Gemma 3 via Ollama local server
        response = ollama.chat(
            model='gemma3:4b', 
            messages=[{'role': 'user', 'content': prompt}]
        )
        print("\n" + response['message']['content'])
    except Exception as e:
        print(f"\n⚠️ Could not connect to Ollama: {e}")
        print("Make sure 'ollama serve' is running in the background and you have pulled the model using 'ollama run gemma3:4b'.")

if __name__ == "__main__":
    main()
