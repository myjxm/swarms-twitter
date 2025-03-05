create table tweet_user(
id varchar(50) primary key not null, -- 'The unique identifier of the user.',
create_date date not null, -- 'The date and time when the user account was created.',
name varchar(50) not null, -- 'The user's name.',
url   varchar(50),  -- 'The user's URL.'
location varchar(30), -- ' The user's location information.',
description varchar(100), -- 'The user's profile description.',
is_blue_verified bool, -- 'Indicates if the user is verified with a blue checkmark.',
verified bool, --'Indicates if the user is verified.',
can_dm bool, --'Indicates whether the user can receive direct messages.',
followers_count int,  -- 'The count of followers.',
fast_followers_count  int,  -- 'The count of fast followers.',
normal_followers_count int,  -- 'The count of normal followers.',
following_count   int,  -- 'The count of users the user is following.',
dw_snsh_dt  date not null  -- 'Date of statistics'
)

create table tweet_tweet(
    id  varchar(50) primary key ,--The unique identifier of the tweet.
    created_date date ,-- The date and time when the tweet was created.
    created_at_datetime timestamp, --The created_at converted to datetime.
    user_id  varchar(50), --Author of the tweet.
    quote_count int,--The count of quotes for the tweet.
    reply_count int,--The count of replies to the tweet.
    favorite_count int,--The count of favorites or likes for the tweet.
    view_count  int,--The count of views.
    retweet_count int --The count of retweets for the tweet.
)

