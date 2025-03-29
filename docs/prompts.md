# Prompts for gro_Grok_Template

## Condense Prompt
"Condense this detailed description into a succinct summary, retaining the main facts and key details, and omitting unnecessary elaboration to create a compact overview."

## General Expand Prompt
"Expand this condensed version into a detailed description, using the main facts and key details provided as the foundation, and infer additional context where needed to create a coherent overview."

## State.json Expand Prompt
"Expand this condensed version into a detailed technical description, using the main facts and key details provided in the state.json as the foundation. Infer additional context where needed to enhance clarity, focusing on the project's no-API, modular design and live testing process, to create a coherent and procedural overview."

## Chat Prompt Tools

- **#ccMod (Chat Condense Mode)**: When requested, add a list of actions at the bottom of the reply with a "We are here: Step X" marker. Focus replies on the current step(s). As steps are completed, I’ll delete them, update "We are here:", and post the new step. Update the list in your reply, remembering the last step. `#ccModEnd` exits this mode. This saves time by avoiding repeated information.

**#Action:**:When I request **#Action:** (Action: replies) for when the user is given actions to perform, clearly differentiate the bold labelled **#Actions:** from other non-action content. This speeds up user interaction. **#Actions:** mode will be the default. Add this prompt if Grok loses memory or hallucinates.

**#Copy**: Enables "Copy" buttons on individual action replies for one-click copy-paste to VS Code IDE. Set as default mode. Re-add if Grok loses memory or hallucinates.

**“#Important #e1 Details to Remember:”** “#Important #e1 Details to Remember:”section, sourced from your provided list (originally derived from the last 5 #e1 chats), is checked for updates with every chat but modified only upon explicit request (e.g., “add/remove detail” or “refresh”). It’s posted in every reply under a bold heading. The list is dynamically updated via requests, with the ability to remove captured or completed details. This setup keeps key project principles visible and is flexible for future adjustments.