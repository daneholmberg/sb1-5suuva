import { Client, GatewayIntentBits } from 'discord.js';
import { config } from 'dotenv';
import { saveMessage, getLastMessageId } from './db.js';

config();

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.GuildMessages
  ]
});

const CHANNEL_ID = process.env.CHANNEL_ID;
const FETCH_LIMIT = 100;
const INTERVAL = 60000; // 1 minute

async function fetchMessages(channelId, beforeId = null) {
  const channel = await client.channels.fetch(channelId);
  if (!channel) {
    console.error('Channel not found');
    return;
  }

  const options = { limit: FETCH_LIMIT };
  if (beforeId) {
    options.before = beforeId;
  }

  try {
    const messages = await channel.messages.fetch(options);
    if (messages.size === 0) {
      return false;
    }

    for (const message of messages.values()) {
      saveMessage(message);
    }

    return true;
  } catch (error) {
    console.error('Error fetching messages:', error);
    return false;
  }
}

async function scrapeChannel(channelId) {
  console.log(`Starting to scrape channel: ${channelId}`);
  
  let hasMore = true;
  let lastMessageId = getLastMessageId(channelId);

  while (hasMore) {
    hasMore = await fetchMessages(channelId, lastMessageId);
    if (hasMore) {
      lastMessageId = getLastMessageId(channelId);
      console.log(`Fetched batch of messages before ID: ${lastMessageId}`);
    }
  }

  console.log('Reached end of channel history');
}

async function startScraping() {
  while (true) {
    await scrapeChannel(CHANNEL_ID);
    console.log(`Waiting ${INTERVAL/1000} seconds before next scan...`);
    await new Promise(resolve => setTimeout(resolve, INTERVAL));
  }
}

client.once('ready', () => {
  console.log(`Logged in as ${client.user.tag}`);
  startScraping().catch(console.error);
});

client.login(process.env.DISCORD_TOKEN);