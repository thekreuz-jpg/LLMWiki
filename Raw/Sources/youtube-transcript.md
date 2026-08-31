---
Title: "Open Knowledge Format and the Future of LLM Wikis"
Author: "Wanderloots"
Reference: "https://www.youtube.com/watch?v=T33iI6izAKw"
ContentType:
  - "markdown"
Created: 2026-08-31
Processed: true
tags:
  - "source"
---

# Open Knowledge Format and the Future of LLM Wikis

## Summary

This video covers Google's Open Knowledge Format (OKF) as a standard for building and sharing LLM wikis. It builds on Andrej Karpathy's original LLM wiki concept, addressing the problem of inconsistent wiki structures across different users. OKF standardizes both folder organization and metadata fields so agents can reliably consume and produce knowledge bases.

## Key Claims

- Karpathy's LLM wiki gist reached 40,000 stars and made it easy for anyone to build a personal knowledge base with an AI coding agent
- The main problem: everyone builds their own LLM wiki differently, making it impossible to share wikis between agents/people
- OKF solves this by standardizing folder structure and metadata fields (type is the only required field)
- OKF enables "bundles" — packaged wikis that can be shared and consumed by any agent that understands the standard
- The PIV loop (Plan, Implement, Validate) is taught as the primary mental model for AI coding
- Context engineering is identified as the single most important concept for getting reliable code from AI coding assistants
- Even if OKF doesn't become the final standard, something like it will be necessary for agent-to-knowledge-base communication

## Transcript

0:00 A couple months ago, Andre Karpathy released the idea of the LLM wiki. It's a pattern for building personal knowledge bases using LLMs and it totally took off and for good reason. There's a lot of power in the simplicity here. So, this single markdown document in GitHub called it gist got to 40,000 stars. And seriously, you can take this file, copy it, paste it into your coding agent, and ask it to build you an LLM wiki and it's going to be able to just basically oneshot it.

0:31 The idea here is when we're building a personal knowledge base for our second brain, instead of just dumping in a bunch of documents or indexing things for rag, we can have the LLM help us build something smarter, incrementally building and maintaining a persistent wiki with structured interlink collections of markdown files.

0:50 As we're adding in more sources over time like meeting transcripts, plan documents, articles from online, it's going to not just index it, but it's going to read each file, extract key information, and integrate it into the existing wiki. So updating things like the entity pages that it creates over time, so we have that knowledge graph for agent to traverse through and remember all the important information that we're bringing in.

1:21 The main problem that we have here is when you take this gist and you build your own version of an LLM wiki, it's going to be structured differently than the next person doing the same thing. There's no standard. And so, there's really not a way to share your LLM wiki with someone else.

1:56 Your agent doesn't know exactly how I've structured my wiki with the different metadata and my entity files, it's not going to be able to search through it optimally. We need a standard so that everyone's building wikis in the same way so that we can share them freely.

2:12 That is what Google has released here with their open knowledge format. It is a beautifully simple thing just like Karpathy's LLM wiki idea where it's just a simple standard built on top so that you can guarantee you're building your wiki in a way where other people's second brains can understand it and vice versa.

3:23 There are two things that they're standardizing here. The first is how we are organizing information like our entity documents and our concepts. And then the second standardization is the exact fields that we're going to have in our metadata. So this is the information that we tag at the top of every single document to give the agent a richer set of information.

4:00 At the top of every single wiki is your index file. You have the agent maintain this every single time it's bringing new information in. And the index file, it reads this when it's first searching through your knowledge base, pretty much every single time. And so this just gives you a high-level overview of all the documents that you have access to in the wiki.

5:03 We also have the metadata like the title and the tags so that it can also search based on this like if it wants to look at the category of security then it can filter out just those documents. Then we have the full sort of like skill.md here this is like progressive disclosure where the index tells it the knowledge it has and then it can read the full document if it's appropriate.

5:17 We also link to related concepts down here and that link is what really gives us this graph view where you can see how all of our entities and other documents are connected together. So the agent can sift through this to really get a comprehensive set of information if the question really calls for it.

6:05 As much as they're good at this, they aren't going to create this system in the same way that someone else will with their LLM. The way that we link related concepts might be different. The way we structure information, even the metadata, like what if we don't have tags, but we have a field called categories. I mean, even something as simple as that, that little change might make it so that if I gave the knowledge base to another person's agent, it wouldn't know how to search through things categorically.

6:49 If you want to build with OKF, create a new knowledge base with this format or even refactor one to use the open knowledge format, look no further than their spec.md file. This is just like Karpathy's gist where you copy this document. Like you literally just click this one button right here, put it into your coding agent, and tell it to either build you a wiki following the open knowledge format or even refactor an existing one.

7:24 Here is the terminology. Here's how we structure the bundles. Here is how we build the YAML front matter. different attributes that we have for each one of our documents like the tags for categorization. This single source of truth is all that it needs.

8:05 You can specifically ask it to use sub agents to work through the different sections of your knowledge base to refactor it to this format. So really easy to scale, really easy to just have the agent rip through this spec.

9:41 This really is the future of personal agents. It's like what MCP did for agent-to-tool communication, this OKF is doing for agent-to-knowledge-base communication.

10:01 One of the most interesting things to think about here is yes, this is fantastic for sharing knowledge bases or having a teamwide knowledge base. This is also really good though even if you're never going to share a knowledge base. If everybody has the same standard for how they are building up their own personal knowledge base, everyone can share ideas more like, oh, here are the entity pages that are working really well for me and this is how I want to organize things under the standard.

11:01 Sharing wikis with other people is the biggest benefit of OKF. And that leads me into the example that I have for you that's also a gift I'm very excited to share. I have built a bundle, that's what you call an OKF Wiki, that packages up all of my favorite AI coding YouTube videos on my channel.

11:41 I actually want to start doing this so that you can very easily bring it into your second brain and ask questions as it relates to what you actually care about or what you are working on specifically. All you have to do is first of all take this spec and give it to your coding agent. You have it teach itself OKF. And then you go to this repo with my AI coding knowledge bundle. And you just paste this prompt into your coding agent.

12:55 Something that I do for my second brain, every single system that I build in, I always have a top-level document that talks about how it works. Like this is how I'm working with OKF bundles. And then here are the different bundles that I have. So I basically have an index so it knows the different bundles that it can go into and search and read the index that we have in there.

13:16 I also built a simple CLI script. This is actually there in the example bundle that you can clone that makes it easy for it to in the command line list out my bundles to view a specific index and then you know once it finds one of those files it wants to read then we have the command line tool to read by a specific bundle and concept ID.

14:06 There's only four videos, but these are like the best and most up-to-date ones on my channel for AI coding. And then I have the concepts as well. So different things that I talk about throughout multiple of the videos that I want to extract into its own entity page.

14:47 The PIV loop, for example, this is the primary mental model that I always teach for AI coding. Very important to have a process for yourself to plan, implement, and validate whatever you're creating with a coding agent.

15:02 The type, this is what is required by OKF. It is the single required field in the metadata because this is what gives categorization to your documents. If I go to a video here, the type is video. So we can search over just the videos over just the concepts which is especially powerful once you get bundles that are a lot bigger than this.

15:26 We also have all of the optional titles in OKF. So title, tags, related videos. This is how we link things together. Each one of these are optional. Only type is required in OKF.

16:29 I just asked what bundles do I have? It ran a command here. So it used that little CLI tool to list out all the bundles that I have. And then it told me that and then I just asked it a question. So not even telling it what bundle specifically to look through. I said, "What's Cole's single biggest idea for getting reliable code out of an AI coding assistant?" and it ran four commands in total.

16:52 First of all it decided to read the coal AI coding index that's the GitHub that I have for you and then based on the index it knew like okay let's take a look at the concepts here and then from the concepts it's like okay the single most important thing I don't know what in the index told it that but it's like context engineering let's read the concept of context engineering.

17:21 Just beautiful to watch it work. When we have something structured like this, it's so easy for it to start with really not much context at all and then drill down into exactly what we need. That's what OKF gives us as a standard.

17:43 The one critique that I think is actually pretty valid with OKF is a lot of people are saying that it's too simple, right? like there's not a lot of value or substance that's actually added on top of the Karpathy wiki. I think it's kind of valid because if we look at like what it's really doing on top of the Karpathy wiki, it's speaking to like exactly how you organize your different files.

18:09 They specifically have like indexes within the folders and a top level index like you saw in my bundle. I mean, that's something I didn't really have in wikis before. And then we have the specific fields in our metadata like the type is required. The other ones are optional but these are the ones that they recommend. Like that's pretty much it. It's how we organize and what is the metadata.

18:41 I think that's also the point, right? minimally opinionated. It's the bare minimum layer that we need on top so that we can produce and consume these wikis in exactly the same way across everyone's agents that lean into OKF. I think that's actually a good thing. I think that's a benefit, not a downside.

## Notes

- The video references Karpathy's original LLM wiki gist and Google's OKF spec
- The creator shares an "AI coding knowledge bundle" as an example OKF implementation
- The PIV loop and context engineering are highlighted as key concepts for AI coding
- OKF is positioned as the knowledge-base equivalent of MCP for tool communication
