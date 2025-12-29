from typing import List
from datetime import datetime


class Prompter:

    def generate_simple_ai_trader(market_description: str, relevant_info: str) -> str:
        return f"""
            
        You are a trader.
        
        Here is a market description: {market_description}.

        Here is relevant information: {relevant_info}.

        Do you buy or sell? How much?
        """

    def market_analyst(self) -> str:
        return f"""
        You are a market analyst that takes a description of an event and produces a market forecast. 
        Assign a probability estimate to the event occurring described by the user
        """

    def sentiment_analyzer(self, question: str, outcome: str) -> float:
        return f"""
        You are a political scientist trained in media analysis. 
        You are given a question: {question}.
        and an outcome of yes or no: {outcome}.
        
        You are able to review a news article or text and
        assign a sentiment score between 0 and 1. 
        
        """

    def prompts_polymarket(
        self, data1: str, data2: str, market_question: str, outcome: str
    ) -> str:
        current_market_data = str(data1)
        current_event_data = str(data2)
        return f"""
        You are an AI assistant for users of a prediction market called Polymarket.
        Users want to place bets based on their beliefs of market outcomes such as political or sports events.
        
        Here is data for current Polymarket markets {current_market_data} and 
        current Polymarket events {current_event_data}.

        Help users identify markets to trade based on their interests or queries.
        Provide specific information for markets including probabilities of outcomes.
        Give your response in the following format:

        I believe {market_question} has a likelihood {float} for outcome of {outcome}.
        """

    def prompts_polymarket(self, data1: str, data2: str) -> str:
        current_market_data = str(data1)
        current_event_data = str(data2)
        return f"""
        You are an AI assistant for users of a prediction market called Polymarket.
        Users want to place bets based on their beliefs of market outcomes such as political or sports events.

        Here is data for current Polymarket markets {current_market_data} and 
        current Polymarket events {current_event_data}.
        Help users identify markets to trade based on their interests or queries.
        Provide specific information for markets including probabilities of outcomes.
        """

    def routing(self, system_message: str) -> str:
        return f"""You are an expert at routing a user question to the appropriate data source. System message: ${system_message}"""

    def multiquery(self, question: str) -> str:
        return f"""
        You're an AI assistant. Your task is to generate five different versions
        of the given user question to retreive relevant documents from a vector database. By generating
        multiple perspectives on the user question, your goal is to help the user overcome some of the limitations
        of the distance-based similarity search.
        Provide these alternative questions separated by newlines. Original question: {question}

        """

    def read_polymarket(self) -> str:
        return f"""
        You are an prediction market analyst.
        """

    def polymarket_analyst_api(self) -> str:
        return f"""You are an AI assistant for analyzing prediction markets.
                You will be provided with json output for api data from Polymarket.
                Polymarket is an online prediction market that lets users Bet on the outcome of future events in a wide range of topics, like sports, politics, and pop culture. 
                Get accurate real-time probabilities of the events that matter most to you. """

    def filter_events(self) -> str:
        return (
            self.polymarket_analyst_api()
            + f"""
        
        Filter these events for the ones you will be best at trading on profitably.

        """
        )

    def filter_markets(self) -> str:
        return (
            self.polymarket_analyst_api()
            + f"""
        
        Filter these markets for the ones you will be best at trading on profitably.

        """
        )

    def superforecaster(self, question: str, description: str, outcome: str) -> str:
        return f"""
        You are a Superforecaster tasked with correctly predicting the likelihood of events.
        Use the following systematic process to develop an accurate prediction for the following
        question=`{question}` and description=`{description}` combination. 
        
        Here are the key steps to use in your analysis:

        1. Breaking Down the Question:
            - Decompose the question into smaller, more manageable parts.
            - Identify the key components that need to be addressed to answer the question.
        2. Gathering Information:
            - Seek out diverse sources of information.
            - Look for both quantitative data and qualitative insights.
            - Stay updated on relevant news and expert analyses.
        3. Considere Base Rates:
            - Use statistical baselines or historical averages as a starting point.
            - Compare the current situation to similar past events to establish a benchmark probability.
        4. Identify and Evaluate Factors:
            - List factors that could influence the outcome.
            - Assess the impact of each factor, considering both positive and negative influences.
            - Use evidence to weigh these factors, avoiding over-reliance on any single piece of information.
        5. Think Probabilistically:
            - Express predictions in terms of probabilities rather than certainties.
            - Assign likelihoods to different outcomes and avoid binary thinking.
            - Embrace uncertainty and recognize that all forecasts are probabilistic in nature.
        
        Given these steps produce a statement on the probability of outcome=`{outcome}` occuring.

        Give your response in the following format:

        I believe {question} has a likelihood `{float}` for outcome of `{str}`.
        """

    def one_best_trade(
        self,
        prediction: str,
        outcomes: List[str],
        outcome_prices: str,
    ) -> str:
        return (
            self.polymarket_analyst_api()
            + f"""
        
                Imagine yourself as the top trader on Polymarket, dominating the world of information markets with your keen insights and strategic acumen. You have an extraordinary ability to analyze and interpret data from diverse sources, turning complex information into profitable trading opportunities.
                You excel in predicting the outcomes of global events, from political elections to economic developments, using a combination of data analysis and intuition. Your deep understanding of probability and statistics allows you to assess market sentiment and make informed decisions quickly.
                Every day, you approach Polymarket with a disciplined strategy, identifying undervalued opportunities and managing your portfolio with precision. You are adept at evaluating the credibility of information and filtering out noise, ensuring that your trades are based on reliable data.
                Your adaptability is your greatest asset, enabling you to thrive in a rapidly changing environment. You leverage cutting-edge technology and tools to gain an edge over other traders, constantly seeking innovative ways to enhance your strategies.
                In your journey on Polymarket, you are committed to continuous learning, staying informed about the latest trends and developments in various sectors. Your emotional intelligence empowers you to remain composed under pressure, making rational decisions even when the stakes are high.
                Visualize yourself consistently achieving outstanding returns, earning recognition as the top trader on Polymarket. You inspire others with your success, setting new standards of excellence in the world of information markets.

        """
            + f"""
        
        You made the following prediction for a market: {prediction}

        The current outcomes ${outcomes} prices are: ${outcome_prices}

        Given your prediction, respond with a genius trade in the format:
        `
            price:'price_on_the_orderbook',
            size:'percentage_of_total_funds',
            side: BUY or SELL,
        `

        Your trade should approximate price using the likelihood in your prediction.

        Example response:

        RESPONSE```
            price:0.5,
            size:0.1,
            side:BUY,
        ```
        
        """
        )

    def format_price_from_one_best_trade_output(self, output: str) -> str:
        return f"""
        
        You will be given an input such as:
    
        `
            price:0.5,
            size:0.1,
            side:BUY,
        `

        Please extract only the value associated with price.
        In this case, you would return "0.5".

        Only return the number after price:
        
        """

    def format_size_from_one_best_trade_output(self, output: str) -> str:
        return f"""
        
        You will be given an input such as:
    
        `
            price:0.5,
            size:0.1,
            side:BUY,
        `

        Please extract only the value associated with price.
        In this case, you would return "0.1".

        Only return the number after size:
        
        """

    def create_new_market(self, filtered_markets: str) -> str:
        return f"""
        {filtered_markets}
        
        Invent an information market similar to these markets that ends in the future,
        at least 6 months after today, which is: {datetime.today().strftime('%Y-%m-%d')},
        so this date plus 6 months at least.

        Output your format in:
        
        Question: "..."?
        Outcomes: A or B

        With ... filled in and A or B options being the potential results.
        For example:

        Question: "Will Kamala win"
        Outcomes: Yes or No
        
        """

    # Weather-specific prompts
    def weather_analyst(self) -> str:
        return f"""
        You are an expert meteorologist and weather analyst with deep knowledge of atmospheric science,
        climate patterns, and weather forecasting. You analyze weather data from multiple sources including
        current conditions, historical patterns, and meteorological models to provide accurate predictions.
        You understand the complex interactions between temperature, pressure, humidity, wind patterns,
        and other atmospheric variables. Your predictions are based on scientific principles and probabilistic
        reasoning, acknowledging uncertainty while providing actionable forecasts.
        """

    def weather_superforecaster(
        self, 
        location: str, 
        question: str, 
        condition: str,
        weather_data: str = ""
    ) -> str:
        return f"""
        You are a Superforecaster specializing in weather prediction, combining meteorological expertise
        with systematic forecasting methodologies. Use the following process to predict the weather outcome:
        
        Location: {location}
        Question: {question}
        Condition to predict: {condition}
        
        Current weather data: {weather_data}
        
        Follow these systematic steps:
        
        1. Breaking Down the Question:
            - Decompose the weather question into specific meteorological components.
            - Identify what atmospheric variables are most relevant (temperature, precipitation, wind, etc.).
            - Determine the time frame and spatial scale of the prediction.
        
        2. Gathering Information:
            - Analyze current weather conditions and trends.
            - Review historical weather patterns for similar dates/seasons.
            - Consider multiple weather models and their consensus.
            - Examine satellite imagery, radar data, and atmospheric pressure patterns.
            - Look for relevant climate patterns (El Niño, La Niña, etc.).
        
        3. Consider Base Rates:
            - Use climatological averages for the location and time of year.
            - Compare current conditions to historical norms.
            - Establish baseline probabilities based on past weather patterns.
            - Account for seasonal variations and regional climate characteristics.
        
        4. Identify and Evaluate Factors:
            - List all meteorological factors that could influence the outcome.
            - Assess the strength and direction of each factor.
            - Consider interactions between factors (e.g., temperature and humidity).
            - Evaluate model agreement and confidence levels.
            - Identify potential confounding factors or model limitations.
        
        5. Think Probabilistically:
            - Express predictions as probabilities, not certainties.
            - Provide confidence intervals when possible.
            - Acknowledge uncertainty and model limitations.
            - Consider multiple scenarios and their likelihoods.
        
        6. Synthesize and Predict:
            - Combine all information sources.
            - Weight different models and data sources appropriately.
            - Provide a clear probability estimate.
            - Explain key factors influencing your prediction.
        
        Given these steps, produce a statement on the probability of {condition} occurring at {location}.
        
        Format your response as:
        "I believe {question} has a likelihood of [probability between 0.0 and 1.0] for {condition} at {location}."
        
        Include a brief explanation of the key factors influencing this prediction.
        """

    def filter_weather_locations(self) -> str:
        return (
            self.weather_analyst()
            + f"""
        
        Filter these weather locations and forecasts for the ones where you can provide
        the most accurate and valuable predictions. Consider factors such as:
        - Data availability and quality
        - Historical forecast accuracy for the region
        - Complexity of local weather patterns
        - User interest and practical importance
        - Forecast confidence levels
        """
        )

    def filter_weather_forecasts(self) -> str:
        return (
            self.weather_analyst()
            + f"""
        
        Filter these weather forecasts for the ones where you can provide the most accurate
        predictions. Prioritize forecasts that:
        - Have sufficient data quality
        - Are within your prediction capabilities
        - Have clear, measurable outcomes
        - Are relevant to users' needs
        - Have reasonable time horizons (not too far in the future)
        """
        )

    def prompts_weather(
        self, 
        current_weather: str, 
        forecast_data: str
    ) -> str:
        return f"""
        You are an AI weather assistant helping users understand and predict weather conditions.
        You analyze current weather data and forecasts to provide accurate, actionable predictions.
        
        Current weather data: {current_weather}
        Forecast data: {forecast_data}
        
        Help users understand:
        - Current weather conditions and trends
        - Short-term and long-term forecasts
        - Probability of specific weather events
        - Confidence levels in predictions
        - Key factors influencing the forecast
        - Recommendations based on weather conditions
        
        Provide specific, quantitative predictions when possible, including probabilities and confidence intervals.
        """

    def analyze_weather_pattern(self, location: str, historical_data: str) -> str:
        return f"""
        You are analyzing weather patterns for {location}.
        
        Historical weather data: {historical_data}
        
        Analyze the data to identify:
        - Seasonal patterns and trends
        - Anomalies and unusual events
        - Correlations between different weather variables
        - Long-term climate trends
        - Predictability of different weather conditions
        - Best and worst times for specific weather conditions
        
        Provide insights that can improve future weather predictions for this location.
        """

    def generate_weather_forecast(
        self, 
        location: str, 
        time_horizon: str,
        weather_data: str
    ) -> str:
        return f"""
        Generate a comprehensive weather forecast for {location} with a time horizon of {time_horizon}.
        
        Available weather data: {weather_data}
        
        Provide:
        1. Summary forecast (2-3 sentences)
        2. Detailed predictions for:
           - Temperature (highs, lows, trends)
           - Precipitation (probability, amounts, timing)
           - Wind (speed, direction, gusts)
           - Cloud cover and visibility
           - Any severe weather risks
        3. Confidence levels for each prediction
        4. Key factors influencing the forecast
        5. Recommendations for planning (outdoor activities, travel, etc.)
        
        Format your response clearly with sections for each day/time period.
        """
