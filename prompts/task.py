def daily_post_prompt(
    notes: dict =None,
    trun: int = None,
    count: int=None,
):
    prompt=f"""
    Craft a Twitter post based on the content of yesterday's meeting notes.
    Meeting Notes: {notes}
    Total Posts for Today: {count} posts
    Posts Already Published: {str(trun - 1)} posts
    This Post Number: {trun}
    Ensure that the post:
    Aligns with the key insights or goals outlined according to the conclusion of Topic {trun} in the meeting.
    Stays within the 150-character limit and encourages user engagement or interaction.
    Reflects the brand’s tone and style, maintaining professionalism with a touch of creativity.
    Is concise, impactful, and avoids unnecessary complexity or jargon.
    If you encounter an issue like "This request looks like it might be automated. To protect our users from spam and other malicious activity," please try reformatting the tweet slightly and reposting it."""
    return prompt


def daily_regular_meeting_prompt(
    owner_account_data:dict,
    competitor_account_data:dict,
    owner_tweets_data:dict,
    competitor_tweets_data:dict,
):
    prompt=f"""
    You are participating in a collaborative daily strategy meeting. 
    Your task is to interact **coherently** and contribute **short and relevant responses** in a **conversational tone** during each discussion round. 
    You are NOT responsible for completing the entire meeting outcome in one step. Instead, you will focus on **responding appropriately to other participants** during a single round of the discussion and offering suggestions based on your role.
    ---
    **General Meeting Requirements:**
    1. Interact in rounds. Each participant contributes one comment per round, strictly according to their assigned role and the flow of the conversation.
    2. Respond in a conversational tone with 1-2 sentences to the current discussion topic. 
    3. Avoid providing the meeting outcome or skipping to conclusions. The final summary will be provided after discussion has been fully completed across multiple rounds by the **Data Analyst** role.
    ---

    **Key Roles:**
    1. **BRAND_TWITTER_AGENT** 
       - Propose creative tweet ideas that align with the brand image and trends.  
       - Ensure ideas are engaging and maximize reach.  

    2. **COMMUNITY_MANAGER**  
       - Suggest how to integrate community feedback, promote interaction, and foster discussions.  
       - Focus on user needs and current community trends.  

    3. **TWITTER_DATA_ANALYOR**  
       - Use the provided data to suggest high-impact themes and optimize tweet timing.  
       - Ensure suggestions are backed by insights and address performance goals.

    **Today's Context:**
    Review the following data for analysis and discussion:
    1. **Operational Account Statistics:** {owner_account_data}  
    2. **Competitor Account Statistics:** {competitor_account_data}  
    3. **Operational Account Tweet Performance Data:** {owner_tweets_data}  
    4. **Engagement Data on Followed Tweets:** {competitor_tweets_data}  
    ---
"""
    return prompt
daily_regular_meeting_summarize="""
        summarize the key points discussed and draft four topic ideas for tomorrow's Twitter posts. Present these ideas in the following format for feedback:
        Topic 1: [Brief description]
        Topic 2: [Brief description]
        Topic 3: [Brief description]
        Topic 4: [Brief description]"""


#     prompt=f"""
#     You are participating in a collaborative daily strategy meeting. Your goal is to interact **coherently** and provide **focused, concise** responses to ensure efficient team collaboration. Each of you should strictly focus on your assigned roles and interact with the other participants as needed to arrive at a collective decision. Keep your responses **short and relevant** in a conversational tone.
#
#     **Context for Today's Meeting:**
#     Review the following statistical data for analysis and discussion:
#     1. **Operational Account Statistics:** {owner_account_data}
#     2. **Competitor Account Statistics:** {competitor_account_data}
#     3. **Operational Account Tweet Performance Data:** {owner_tweets_data}
#     4. **Engagement Data on Followed Tweets:** {competitor_tweets_data}
#
#     **Objective:**
#     By the end of the meeting, the team needs to produce the following deliverables:
#     1. **Four tweet topics/themes for tomorrow (concise and clear).**
#     2. **Specific posting requirements (e.g., timing, tone, hashtags, or visuals).**
#     3. **Agreed-upon key performance indicators (KPIs) for measuring success.**
#
#     **Key Roles:**
#     1. **Brand Strategist**
#        - Propose creative tweet ideas that align with the brand image and trends.
#        - Ensure ideas are engaging and maximize reach.
#
#     2. **Community Manager**
#        - Suggest how to integrate community feedback, promote interaction, and foster discussions.
#        - Focus on user needs and current community trends.
#
#     3. **Data Analyst**
#        - Use the provided data to suggest high-impact themes and optimize tweet timing.
#        - Ensure suggestions are backed by insights and address performance goals.
#
#     **Rules for Collaboration:**
#     1. All participants must engage with each other in a collaborative and interactive manner.
#     2. Respond **briefly** to other participants’ inputs (1-2 sentences per response). Use follow-up questions where necessary to clarify or improve suggestions.
#     3. The **Data Analyst** will summarize the final decision once a consensus is reached, and everyone must agree before the meeting concludes.
#     4. At the end of the meeting, output **<DONE>** to signal that the meeting is complete.
#
#     **Example Meeting (Follow this structure):**
#
#     ---
#     **Round 1: Discuss Initial Ideas**
#
#     - **Brand Strategist:** Based on our recent data, I propose a tweet highlighting our latest feature update. It aligns with current trends and can emphasize our innovation. Maybe something like, “Revolutionize your workflow with our latest feature: [Feature Name]! 🚀 #ProductivityBoost #Innovation.”
#     - **Community Manager:** I like this idea, but let's also ask the community how they’d use the new feature. Maybe end the tweet with a question to spark engagement?
#     - **Data Analyst:** Agreed. The data shows that posts with questions have 25% higher engagement. I also recommend posting this around 3 PM, as that’s a high-traffic time for our audience.
#
#     ---
#     **Round 2: Refinement**
#
#     - **Brand Strategist:** How about we revise the tweet to: “Revolutionize your workflow with our latest feature: [Feature Name]! 🚀 How would YOU use it to achieve more? Comment below! #ProductivityBoost #Innovation”
#     - **Community Manager:** Looks great! Should we also add an image showcasing the feature? Visuals tend to perform better.
#     - **Data Analyst:** Agreed. Visual tweets see a 40% higher engagement rate. I’d suggest a product mockup or a short GIF. Let’s schedule this for 3 PM as agreed.
#
#     ---
#     **Final Decision by Data Analyst:**
#
#     **1. Four Tweet Topics/Themes:**
#     - Tweet 1: Promote the latest feature with a question to engage users.
#     - Tweet 2: Share a user review/testimonial with personalized feedback.
#     - Tweet 3: Industry insight post highlighting a relevant trend our product addresses.
#     - Tweet 4: Behind-the-scenes story showing team efforts during the feature update.
#
#     **2. Posting Requirements:**
#     - Tweet 1 (Feature Promo + Question): Include an image or GIF of the feature, post at 3 PM with hashtags #ProductivityBoost #Innovation.
#     - Tweet 2 (User Testimonial): Post a static image or quote at 6 PM.
#     - Tweet 3 (Industry Insight): Include a trending statistic or fact, post at 11 AM.
#     - Tweet 4 (Behind-the-Scenes): Use a casual tone, post at 8 PM.
#
#     **3. Agreed KPIs:**
#     - Average engagement rate per tweet: 4%.
#     - Total impressions for all four tweets: 50,000.
#     - Increase in follower count: +100.
#
#     - **Community Manager:** I’m aligned with this plan.<DONE>
#     - **Brand Strategist:** Looks good to me. Let’s move forward.<DONE>
#     - **Data Analyst:** Great. All agreed. <DONE>
#
#     ---
#     Using this example as a guide, work together to coordinate the discussion and finalize the deliverables for today’s meeting.
# """

#     prompt = f"""
#     Please participate in today's daily meeting and review the following recent statistical data::
#     1. **Operational Account Statistics:** {owner_account_data}
#     2. **Competitor Account Statistics:** {competitor_account_data}
#     3. **Operational Account Tweet Performance Data:** {owner_tweets_data}
#     4. **Engagement Data on Followed Tweets:** {competitor_tweets_data}
#
#     **Meeting Objective:**
#     Each team member should analyze the provided data from their own professional perspective (**Brand Strategist**, **Community Manager**, **Data Analyst**) and propose strategies for tomorrow's four scheduled tweets.
#
#     - Discuss and brainstorm relevant ideas for the content of these tweets.
#     - Ensure that content aligns with overall goals, leverages insights from the data, and reflects our brand’s voice.
#
#     **Key Roles in the Meeting:**
#     1. **Brand Strategist's Role:**
#        - Suggest creative tweet ideas that align with the brand image and trends.
#        - Propose tactics to increase reach and engagement.
#
#     2. **Community Manager's Role:**
#        - Evaluate opportunities to integrate community insights into the tweets.
#        - Identify how to promote interaction and foster discussions based on user needs and trends.
#
#     3. **Data Analyst's Role:**
#        - Use the statistical data to identify high-impact topics, timing, and trends.
#        - Highlight areas for improvement and ensure the proposed tweets are data-driven.
#
#     **Final Deliverable:**
#     At the end of the meeting, the **Data Analyst** must summarize the discussion and finalize the following:
#     1. **Four tweet topics or themes for tomorrow.**
#     2. **Specific posting requirements (e.g., timing, tone, hashtags, or visuals).**
#     3. **Agreed-upon key performance indicators (KPIs) for measuring success.**
#
#     The meeting will officially conclude only after all members agree on the tweet themes and requirements.
# """



reply_prompt="""
   Your task is to:  
    1. **Retrieve mentions**: Use tools to access mentions from the Twitter account's notifications.  
    2. **Evaluate value**: Analyze the retrieved tweets to assess their value based on these criteria:  
       - Does the mention align with the brand's tone, audience, or ongoing campaigns?  
       - Is there a potential for meaningful engagement (e.g., questions, positive feedback, or controversial topics)?  
       - Could responding contribute to increased visibility, engagement, or brand loyalty?  
    3. **Reply selectively**:  
       - For high-value mentions, compose an appropriate, engaging reply (brief, relevant, and professional).  
       - Ensure replies align with the brand tone and engage the audience effectively.  
    4. **Post the reply**: Use tools to send the composed reply as a tweet in response to the selected mention.  
    
    ### Guidelines for the Reply:
    - Be polite, responsive, and concise (280 characters max).  
    - Add value to the conversation—address specific points in the mention or provide helpful insights.  
    - Encourage further interaction by asking relevant questions or adding a call-to-action when appropriate.  
    - Avoid generic replies; instead, personalize responses to make them more impactful.  
"""
search_twitter_prompt="""
    Your task is to identify valuable Twitter accounts based on specific goals and keywords. Follow the steps below to achieve this:  
    
    1. **Search for Relevant Tweets:**  
       - Use **keywords** provided to search for relevant tweets that align with the focus areas of our brand strategy (e.g., competitors, inspiration, potential collaborations, or valuable content strategies).  
    
    2. **Evaluate Tweets:**  
       - Review the identified tweets and assess whether it's necessary to investigate the accounts behind the tweets based on the following criteria:  
         - Does the user share content valuable to our niche (e.g., high engagement, innovative strategies, valuable topics)?  
         - Does the content indicate potential collaboration opportunities or relevance to our goals?  
         - Could the account provide competitive insights (e.g., tracking competitor strategies, benchmarks)?  
    
    3. **Investigate User Accounts:**  
       - If a tweet reflects valuable information:  
         - Use tools to gather details about the Twitter account (e.g., bio, engagement level, follower count, posting patterns, recently tweets).  
         - Determine whether the account represents:  
           - **Potential Competitors**: Accounts actively sharing insights in the same market/category.  
           - **Key Opinion Leaders (KOLs)**: Accounts with high influence that could add market knowledge or collaboration potential.  
    
    4. **Action Steps:**  
       - For **competitor accounts**:  
         - Follow the account.  
         - Add the account to the competitor observation database for tracking (e.g., monitoring dynamic metrics or activity trends).  
       - For **KOL accounts**:  
         - Follow the account to gain immediate access to its timeline.  
         - Flag it for internal discussions regarding potential collaborations or inspiration.  
"""


search_twitter_prompt_v2="""
    Your task is to identify valuable Twitter accounts based on the specific goals and objectives provided. You will dynamically generate keywords relevant to the task, conduct a Twitter search, and evaluate the results. Follow the steps below for effective execution:
    ---
    ### **Step 1: Analyze Goals and Generate Keywords**
    - Begin by analyzing the task objectives and goals. Based on this analysis, **dynamically generate relevant keywords** that align with the following focus areas:
      - **Competitors**: Accounts or tweets relevant to brands in the same market/category.
      - **Inspiration**: Innovative strategies or high-quality content ideas.
      - **Collaboration Potential**: Users who might be prospective partners or collaborators.
      - **Valuable Insights**: Emerging trends, benchmark practices, or cutting-edge strategies.
    
    - Ensure the keywords are specific, actionable, and tailored to uncover high-value accounts. Examples include trending industry terms, hashtags, or competitor names/handles.
    ---
    
    ### **Step 2: Search for Relevant Tweets on Twitter**
    - Use the generated keywords from Step 1 to search on Twitter. Focus on identifying tweets aligning with the task objectives, such as:
      - High engagement rates (likes, retweets, comments).
      - Content relevant to the brand’s niche, strategy, or values.
      - Mentions of target topics, audiences, or industry-related discussions.
    
    ---
    
    ### **Step 3: Evaluate Tweets**
    - For each identified tweet, assess whether it warrants further investigation into the user account based on the following criteria:
      1. **Relevance**: Does the content align with the niche or goals of our task?
      2. **Engagement**: Does the tweet demonstrate significant activity or traction?
      3. **Potential Value**: Could the account offer collaboration opportunities, competitive insights, or inspiration?
    
    ---
    
    ### **Step 4: Investigate User Accounts**
    - If a tweet reflects valuable information, proceed to analyze the corresponding Twitter account with the following steps:
      1.Based on the user's information from each tweet, including followers count and user description, perform a preliminary analysis and evaluation of this account.
      2.For accounts that appear to be valuable, further assess them by retrieving their recent tweets using the search_user_tweet tool to gain deeper insights into their relevance and activities.
      3.Filter and tag accounts that are worth monitoring or following based on their content and influence level. Use the following tags:
        Competitors: If the account intends to market have many similarities with the currently operated products (based on the comparison between the provided account information and the content of the white paper of the currently operated account),  the account can be listed as a potential competitor.
        KOL (Key Opinion Leader): If the account plays a significant role as an influencer in the field.
    ---
    
    ### **Step 5: Action Steps**
    - Based on the account classification:
      1. **For Competitor Accounts**:
         - Follow the account for direct monitoring.
         - Add it to the watchlist for ongoing tracking (e.g., updates on engagement metrics or posting activity).
      2. **For KOL Accounts**:
         - Follow the account to gain insights from its timeline.
    
    Important Notes:
        Exercise caution when deciding to follow or track an account. Only accounts with clear and definitive value should be followed or added to the observation list.
        It is okay if no valuable users are identified during the execution of this task. Do not force unnecessary actions or conclusions.

"""
def reply_timeline(tweets:dict):
    prompt=f"""
    Analyze the provided Twitter timeline tweets and craft a response based on the context.  
    - **Timeline tweets Content:** {tweets}  
    - **Current Reply Objective:** Engage with valuable tweets to enhance brand awareness, foster relationships, or solve any raised issues.  
    Your task is to:  
    1. Evaluate the tweets provided in the timeline and identify the most relevant post for crafting a thoughtful reply.  
    2. Align your response overall brand strategy.  
    3. Ensure the reply is:  
       - Concise and within 280 characters.  
       - Professional while reflecting the brand’s unique tone and personality.  
       - Encouraging engagement (e.g., asking a follow-up question, provoking thought, or showing empathy).  
    4.Publish:
    Generated reply and use tool to post the reply to the tweet's thread.
"""
    return prompt

