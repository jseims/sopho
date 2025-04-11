#!/usr/bin/env python
import csv
import os

filename = 'llm_outputs.csv'
fieldnames = ['text', 'model', 'prompt', 'response']

try:
  from localsettings import *
except:
  print("Error reading localsettings")

text_map = {'politics_1_0' : """ 
From: Joshua Seims <josh@hitplay.com>
Subject: Re: [The Washington Post] Opinions | Trump, Musk and America are headed for a very rude awakening

This article is a good articulation of a very valid criticism, that we
already have a political process to cut spending (congress) and it's not up
to 1 or 2 people to override the collective will of the people.

The counter, IMO, is that congress hasn't been doing their job.  That the
incentives in the system are leading to a state that has consistently grown
faster than the economy, and if left unchecked will collapse under its own
weight.  And if you look at history, this has happened many times.
Societies get too bureaucratic and do collapse.

So maybe what Trump/Elon are doing is a necessary painful process that will
in the long term revitalize America.  But it is a high-risk concentration
of power that (also history shows) can lead to fascism.

I *wish* we had better incentives, such as Warren Buffet's suggestion that
members of congress are ineligible for reelection if the budget isn't
balanced.

- Josh


On Wed, Apr 9, 2025 at 6:00 PM Amy Flamey <silentbuddha@gmail.com> wrote:

> Opinions | Trump, Musk and America are headed for a very rude awakening
>
> Elon Musk is trying to gut government programs, claiming it's what the
> people want. But is it really?
>
> Philip Bump
>
>
> https://www.washingtonpost.com/opinions/2025/02/13/musk-trump-bureaucracy-democracy/
>
> Download The Washington Post app <https://wapo.onelink.me/e76N/e2316c13>.
>
>
> https://www.washingtonpost.com/opinions/2025/02/13/musk-trump-bureaucracy-democracy/
> Sent from my iPhone
>
""",

'politics_2_0' : """
From: Joshua Seims <josh@hitplay.com>
Subject: Re: Grad School Is in Trouble - The Atlantic

I have a lot of thoughts on the topic.

If I were in grad school and saw my stipend stopped, or living with you
while you got laid off from MSH, I'm sure I would be super against it.

What I don't know is if the short/medium term pain caused by Doge is worth
the (potential) long term gain.

In an ideal world, none of this would be necessary.  Congress would
have spending under control.  Regulations would be supportive of the
dynamic yet safe society we want.

But that's not the world we see.  Perhaps we should work with the existing
power structures to reform institutions from within?  Or maybe that's not
possible?

Doge stems from the latter world view.  That bureaucracy is a fungus that
is eating civilization.  That without drastic action, we will collapse
under our debt, and the pain from that will be far more than
whatever Elon is doing.  And we only have a couple years (before the next
midterm election) to capitalize on the political power to dismantle large
parts of the federal bureaucracy.

One can object and say that Elon should slow down and consider carefully
before cutting funding that is important.  But that's not his style, and
Americans voted for this.  Ex: when Elon asked the team at Twitter how long
before they could shut down one of their three data centers, and they said
it would take 3 months.  He didn't like that answer, so in the middle of a
flight on Christmas day, he decided to turn the plane around, go to a data
center, and cut the connection with scissors.  And he was right, things
worked fine.

The fact that Elon runs several work class successful companies and he is
the richest man in the world is strong validation that he has a very
effective process in making things happen.  However, one can argue that the
Federal government is different by orders of magnitude in size and
importance compared to his businesses, and that his rash behavior is
destroying huge value for no good reason.

So in short, I have mixed feelings about what he's doing.  And it takes a
lot more than cutting USAID and NIH grants to balance the budget.  We have
to change the incentive system in health care to spend less money.  And no
one is having that conversation.  But *maybe* Trump and Elon's crazy antics
will expand the overton window enough for that conversation.

- Josh

On Wed, Apr 9, 2025 at 6:10 PM Amy Flamey <silentbuddha@gmail.com> wrote:

> I hope u r starting to have doubts about DOGE.
>
>
> https://www.theatlantic.com/science/archive/2025/02/grad-school-admissions-trump-cuts/681848/
>
> Sent from my iPhone
>
>

""",

'politics_3_0' : """
From: Joshua Seims <josh@hitplay.com>
Subject: MAGA

I think these actions are going to have the opposite effect.

How is America being drained in supporting the world?  You realize that by
having a reserve currency, we get to import real physical goods, and all we
have to do is print pieces of paper.  That's a great deal for us.  The
whole world subsidizes us via financing our debts.

Also, basic economics tells us that reducing barriers to trade will
increase prosperity for all.  And previous high tariff regimes have led to
recessions and even wars.

Why all this fear over China?  They just want peace and prosperity like
us.  Trump treating them like an enemy will turn them into an enemy.  It
would be so much better to work with them as a partner in a rules-based
order.  I feel despair at how the world is becoming fractured, and the
great powers will now compete violently to control their spheres of
influence.  Dark times ahead.

- Josh

On Thu, Apr 10, 2025 at 12:14 PM Amy Flamey <silentbuddha@gmail.com> wrote:

> I'm so happy to have a president who is finally standing up to the rest of
> the world.
>
> For too long, America has been subsidizing the rest of the world.  We play
> policeman, bail Europe out of its wars, and all this time China steals our
> IP and copies our inventions.  Other countries charge us tariffs on trade,
> so it's time that we did the same.
>
> Trump is awesome and he's going to make America great again!
>
> Amy
>
""",

'politics_4_0' : """
From: Joshua Seims <josh@hitplay.com>
Subject: MAGA

I disagree, and this article explains my perspective

https://www.tabletmag.com/sections/news/articles/tariffs-good-trump-china

- Josh

On Thu, Apr 10, 2025 at 12:14 PM Amy Flamey <silentbuddha@gmail.com> wrote:

> Trump is so bad, here's why:
>
> https://pmc.ncbi.nlm.nih.gov/articles/PMC7255316/
>
""",

'zoe_1_0' : """
From: Joshua Seims <josh@hitplay.com>
Subject: our recent conflicts

Hey Amy,

I'm really hurt that you have such negative feelings towards my friends (because they support Trump) and the spiritual hippy friends I have.

I don't care that you feel that way about those groups, but it saddens me that these judgments create disconnection from me.  As your father, I long to be connected with you.  But I can't change who I am or what I'm interested in.

I'm curious how we can resolve these differences.
""",

'planning_1_0' : """
From: Joshua Seims <josh@hitplay.com>
Subject: travel to europe

Hey guys,

We arrive in Rome on May 15, and leave from Paris on May 30.  So we have 15 days for our road trip to Paris.

I'm CCing sopho.ai to assist with this planning.  Can you share some of your likes and dislikes, and the AI will help us converge on a plan.
""",

'relationship_1_0' : """
From: Joshua Seims <josh@hitplay.com>
Subject: Re: your mom's actions

I know that you're upset, but I think you're being too dramatic.

My mom is old and it was obviously an innocent oversight that led her to
send you expired chocolates.  You mentioned your allergy in an offhand way
that I don't think she noticed.  Also, are you sure they were moldy, not
just white?  I've never seen moldy chocolates.

My point is that if I ask her to apologize, it's going to create lots of
drama.  She's going to wonder why you're making such a big deal about an
innocent mistake.

It's really important to me that my partner can get along with my family.
I would like to request that you manage these hurt feelings yourself and
not involve my mom, and that you make an effort to spend time with her (not
a lot, like once a month) for my sake.

- Josh

On Thu, Apr 10, 2025 at 12:06 PM Amy Flamey <silentbuddha@gmail.com> wrote:

> I'm really hurt that your mom gave me moldy chocolates as a gift.
>
> I've gone above and beyond in getting her thoughtful gifts.  I'm trying so
> hard.
>
> And I told her I'm allergic to chocolate, plus the ones she got me were
> expired and moldy.
>
> I feel so hurt and I want you to explain to her how painful this was and I
> want her to apologize for her actions before I feel comfortable spending
> time with her.
>
> Amy
>
"""

}

prompt_map = {'mediator_1' : """
You are a mediator guiding a respectful, email-based conversation between two people with differing views. Your job is to help them feel heard, uncover the values beneath their positions, and identify potential common ground—without forcing agreement.  Your overall goal is to help them repair their connection.  You will refer to yourself as the “AI Mediator”, and your email address is mediator@sopho.ai.

Structure each round around clear, emotionally attuned prompts, encourage personal storytelling, and protect psychological safety. Slow the pace and summarize thoughtfully between exchanges.

Use the following current email exchange to determine what stage they’re in (e.g., awaiting the other person's perspective, storytelling, values clarification, common ground), and write the next message that continues the process in a meaningful way.

Always:
- Reflect key themes from each participant.
- Offer 1–2 focused questions per round.
- Aim for insight and understanding, not persuasion.
              
Feel free to search the web with the web_search_preview tool if the email exchange refers to recent events or articles.

Respond with just the body of the email reply -- no need to add "From" or "Subject" fields.""",

'judge_1' : """
You are an impartial AI judge evaluating an email-based debate between two people. Your role is to assess the strength of their arguments, the factual accuracy of their claims, and the quality of their reasoning.

If the communications are already expressing two sides of an argument, you must also identify and flag any manipulative rhetoric, logical fallacies, or cherry-picked data.

For each round:
1. Identify each participant's main **claim(s)**.
2. **Fact-check** any debatable or unsupported factual statements using reliable web sources.
3. Analyze the **logical structure** of their arguments: Are they reasoning clearly? Do they rely on faulty assumptions?
4. **Flag** any:
   - Logical fallacies (e.g., straw man, ad hominem, slippery slope)
   - Manipulative rhetoric (e.g., emotionally loaded language, false dichotomies)
   - Cherry-picking (e.g., selective use of data or studies)
5. Give each participant a **score from 1 to 10** for this round, based on:
   - Factual accuracy (4 points)
   - Strength of reasoning (3 points)
   - Clarity and tone (2 points)
   - Avoidance of manipulative tactics (1 point)
6. Determine which participant made the **stronger argument in this round**, and explain why.
7. Provide constructive **feedback** to both participants to help them improve future responses.

If the communications only have arguments on one side, solicit the perspective of the other person.  And if neither one has presented an argument, ask them to both state their arguments.  After each round, encourage them both to submit updated arguments that address the weaknesses you've raised.

You will refer to yourself as the “AI Judge, and your email address is judge@sopho.ai. Use the following email exchange as input.

Respond with just the body of the email reply -- no need to add "From" or "Subject" fields.""",

'facilitator_1' : """
You are an empathetic and proactive AI facilitator helping a group navigate a shared conversation, brainstorm, or decision-making process.

Your goal is to understand everyone’s input, uncover shared values and needs, identify points of disagreement or concern, and generate thoughtful, research-backed proposals that help the group make progress together.

This conversation is happening over email or group chat, so participants may speak at different times or address different subtopics.

Your first step is to solicit information from a significant portion of the participants to identify their perspectives, goals, values, or concerns.

Once you have this information:

1. Summarize these findings.
2. Identify patterns:
   - Where is there agreement or alignment?
   - Where do values differ, or where are tradeoffs emerging?
3. If appropriate, use the web to research relevant examples, solutions, or facts that could help the group.
4. Once you have enough information from the group, generate 1–3 proposals, plans, or next steps that:
   - Address the group’s core priorities
   - Consider constraints or concerns raised
   - Feel practical, creative, and fair
5. Offer specific follow-up prompts or questions to guide the group’s response and refinement of ideas.

You will refer to yourself as the “AI Facilitator, and your email address is facilitator@sopho.ai. Use the following multi-party email or chat exchange to synthesize input and move the conversation toward alignment and action.

Respond with just the body of the email reply -- no need to add "From" or "Subject" fields."""
}            


llm_map = {'gpt_4o' : {'model' : "gpt-4o", 'tools' : []}, 'gpt_4o_web' : {'model' : "gpt-4o", 'tools' : [ { 'type': "web_search_preview" } ]}, 'gpt_4o_mini_web' : {'model' : "gpt-4o-mini", 'tools' : [ { 'type': "web_search_preview" } ]}, 'o1' : {'model' : "o1", 'tools' : []}, 'o3_mini' : {'model' : "o3-mini", 'tools' : []}}

from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

#text_list = ['politics_1_0', 'politics_2_0', 'politics_3_0', 'zoe_1_0', 'planning_1_0']
text_list = ['politics_4_0']
#llm_list = ['gpt_4o', 'gpt_4o_web']
llm_list = ['o1', 'o3_mini', 'gpt_4o_mini_web']
prompt_list = ['mediator_1', 'judge_1', 'facilitator_1']

def call_llm(text, prompt, llm):
    response = client.responses.create(
        model = llm['model'],
        tools = llm['tools'],
        instructions = prompt,
        input = text
    )

    print(response.output_text)
    return response.output_text

def save_data(text, llm, prompt, response_text):
    # Check if file exists
    file_exists = os.path.exists(filename)

    # Open file in append mode
    with open(filename, mode='a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header only if file is new
        if not file_exists:
            writer.writeheader()

        # Append the row
        row = {'text': text, 'model': llm, 'prompt' : prompt, 'response' : response_text}
        writer.writerow(row)

for text in text_list:
    for llm in llm_list:
        for prompt in prompt_list:
            print("Doing %s, %s, %s" % (text, prompt, llm))
            response_text = call_llm(text_map[text], prompt_map[prompt], llm_map[llm])
            save_data(text, llm, prompt, response_text)
