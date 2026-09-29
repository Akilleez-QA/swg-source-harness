# Getting involved and getting useful help

> Unofficial independent draft. Not endorsed or adopted by SWG Source. This package implements local static preflight only; proposed trusted intake and integrations remain future work.

You do not need to be an experienced developer to take part. Testing a quest, describing a confusing setup step, or reporting what finally worked can help the next person. When you get stuck, ask with what you know. You do not need to finish an exhaustive investigation first.

## Start with the community rules

Read [rules-and-info](https://discord.com/channels/366560008068005892/818213460612612146), including the [January 2024 behavioral policy](https://discord.com/channels/366560008068005892/818213460612612146/1201676144710262804). It asks that questions be public rather than sent by direct message, explains that participation is voluntary, and prohibits harassment. Keep support questions in the channels; do not send unsolicited support DMs to staff. Public answers also become searchable help for everyone else.

The [community rules](https://discord.com/channels/366560008068005892/818213460612612146/818427167679447050) welcome people from different projects, require civil discussion, and ask you to ask your actual question directly. Instead of “Anyone know about clients?”, try “My client closes before login; where can I find its log?” If a problem concerns a particular live server, start with that server's support team. Mention custom changes when asking about shared source code.

## Find a useful starting channel

These starting points use the channel inventory checked on September 28, 2026. Read the channel topic and recent messages when you arrive; names and availability can change. If you cannot see a channel or are unsure where to post, ask in general.

| Your question or contribution | Starting point |
| --- | --- |
| Where to begin, or where a question belongs | [general](https://discord.com/channels/366560008068005892/366560008608940035) |
| VM, hosting, connectivity or deployment setup | [unofficial-hosting](https://discord.com/channels/366560008068005892/1348810043524513823) |
| In-game administrator commands and tools | [admin_commands](https://discord.com/channels/366560008068005892/366561245077307392) |
| Unexpected behavior or a possible bug | [feedback-bugs](https://discord.com/channels/366560008068005892/441995780459462657) |
| Server/source development | [general_dev_chat](https://discord.com/channels/366560008068005892/366576100941234177) |
| Building or changing the client | [client_build_dev_chat](https://discord.com/channels/366560008068005892/694859723513659463) |
| Windows development | [win-dev-chat](https://discord.com/channels/366560008068005892/772240046731821087) |
| WordPress or Joomla authentication integration | [wordpress-auth](https://discord.com/channels/366560008068005892/701881911462854806) / [joomla-auth](https://discord.com/channels/366560008068005892/1125815902194110504) |
| Modding and asset questions | [mods-and-ends](https://discord.com/channels/366560008068005892/567731005725737011) / [3d-modeling](https://discord.com/channels/366560008068005892/1290442374991970314) |
| Introducing your server or finding teammates | [server-forum](https://discord.com/channels/366560008068005892/1533194140584513699) |

The server-forum's stated purpose is server introductions and team building. Put troubleshooting in the relevant support channel, so an advertisement thread does not become the only place a useful fix can be found. If someone is coordinating a test in [qa-testing](https://discord.com/channels/366560008068005892/449692955524071434), follow that discussion for the requested build and test steps.

## Ask a small, answerable question

A quick search for the exact error or feature name can reveal an existing answer. If the answer is old, does not match your setup, or you do not understand it, say so and ask. Link the guide or message you used rather than saying only “I followed the instructions.”

Share the smallest example you have: what you tried, what you expected, and what happened instead. Exact error text is usually easier to search than a screenshot; screenshots help when the problem is visual. Include a short relevant log excerpt, with passwords, tokens and personal information removed. Keep the full log available if someone asks.

Use as much of this template as you can. “I don't know yet” is a useful answer.

```text
I'm trying to:
I'm using: [VM/release or repository/branch; client version if known]
Steps: [the few actions that show the problem]
Expected:
Actually happened: [exact error or visible behavior]
Already tried: [one or two things and their results]
Guide or earlier discussion:
My question:
```

For example: “I'm setting up the Source VM and can reach character selection, but entering the world hangs. I followed this guide. I haven't changed the source. Which log should I check next?” That is enough to start a useful conversation.

If AI helped, separate what you observed from its proposed explanation. “The log says X; the assistant suspects Y” is more useful than “the assistant proved networking is fine.” Check generated summaries before posting them, and condense long transcripts into the question and relevant evidence.

## Make the conversation easy to continue

The following are suggested habits, not additional official rules: choose one suitable channel first, avoid mass pings and duplicate cross-posts, and allow volunteers time to respond. Keep follow-ups in the same conversation or thread where possible. If you move the question after being redirected, link the original so nobody repeats the same investigation. When following up later, add a useful observation rather than repeatedly asking for attention.

Try a suggested step you understand, then report the result. If it might erase your world, replace local changes, expose credentials, or you simply do not know what it does, ask for an explanation first. It is fine to say “I don't know how to get that log.” A helper can give you a smaller next step.

Close the loop when something works: name the change, the version or setup, and what you tested. If only part works, say which part remains broken. “Rebuilt the native server after updating scripts; the door now opens, but this warning remains” is more useful than “fixed.” Thank the people who helped.

## Contribute at your own pace

You can help by reproducing a report on a known setup, checking a guide's steps, explaining an answer you have verified, or pointing someone to a relevant discussion. The community rules discourage answering when you do not know the answer; avoid presenting a guess as a fix or passing on unverified AI advice.

For a documentation correction, link the page and identify the exact step, your setup, and the wording or result that differed. For a reproducible bug, the posted rules direct reports to [GitHub issues](https://github.com/SWG-Source/dsrc/issues); if you are unsure which repository owns it, ask in feedback-bugs before filing duplicates. A clear report is already a contribution; you do not have to supply the patch.

If you do submit code, read the [AI and modernization policy](https://discord.com/channels/366560008068005892/818213460612612146/1547403437204054096). It requires disclosure of AI involvement in the contribution and, separately, in the PR text. Explain what changed and what you checked so reviewers can assess the work.
