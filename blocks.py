true=True
false=False
class Block:
	option={
		"text": {
			"type": "plain_text",
			"text": "Choice 2",
			"emoji": true
		},
		"value": "value-1"
	}

	releaseSelectionDialog={
	"title": {
		"type": "plain_text",
		"text": "Process Selection"
	},
	"type": "modal",
	"blocks": [
			{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Select a process from your environment. If you don't see your process try running `/run ProcessName`"
			}
		},
		{
			"type": "input",
			"block_id": "envProcess",
			"label": {
				"type": "plain_text",
				"text": "Processes"
			},
			"element": {
				"action_id": "envProcess",
				"type": "static_select"
			}
		}
			
		
		],
		"close": {
			"type": "plain_text",
			"text": ":no_entry_sign: Cancel",
			"emoji": true
		},
		"submit": {
			"type": "plain_text",
			"text": "Select Process"
		},
		"private_metadata": "release",
		"clear_on_close": false,
		"notify_on_close": true
	}


	processSelectionDialog={
		"title": {
			"type": "plain_text",
			"text": "Select a process"
		},
		"type": "modal",
		"blocks": [
			{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Select a process to run."
			}
		},
			{
				"type": "input",
				"block_id": "foundProcess",
				"label": {
					"type": "plain_text",
					"text": "Processes"
				},
				"element": {
					"action_id": "foundProcess",
					"type": "static_select"
					
				}
			}
			
		
		],
		"close": {
			"type": "plain_text",
			"text": ":no_entry_sign: Cancel",
			"emoji": true
		},
		"submit": {
			"type": "plain_text",
			"text": "Select Process"
		},
		"private_metadata": "process",
		"clear_on_close": false,
		"notify_on_close": true
	}


	authDialog={
		"title": {
			"type": "plain_text",
			"text": "Authenticate"
		},
		"type": "modal",
		"blocks": [
			{
				"type": "input",
				"block_id": "tenant",
				"optional": false,
				"label": {
					"type": "plain_text",
					"text": "tenant name"
				},
				"hint": {
					"type": "plain_text",
					"text": "name of your tenant"
				},
				"element": {
					"action_id": "tenant",
					"type": "plain_text_input"
				}
			},
			{
				"type": "input",
				"block_id": "emailOrUsername",
				"optional": false,
				"label": {
					"type": "plain_text",
					"text": "Email or Username"
				},
				"hint": {
					"type": "plain_text",
					"text": "Username to log into your orchestrator instance"
				},
				"element": {
					"action_id": "emailOrUsername",
					"type": "plain_text_input"
				}
			},
			{
				"type": "input",
				"block_id": "password",
				"optional": false,
				"label": {
					"type": "plain_text",
					"text": "Password"
				},
				"hint": {
					"type": "plain_text",
					"text": "password for your orchestrator instance"
				},
				"element": {
					"action_id": "password",
					"type": "plain_text_input"
				}
			},
			{
				"type": "input",
				"block_id": "robot",
				"optional": false,
				"label": {
					"type": "plain_text",
					"text": "robot"
				},
				"hint": {
					"type": "plain_text",
					"text": "name of your robot"
				},
				"element": {
					"action_id": "robot",
					"type": "plain_text_input"
				}
			},
			{
				"type": "input",
				"block_id": "environment",
				"optional": false,
				"label": {
					"type": "plain_text",
					"text": "environment"
				},
				"hint": {
					"type": "plain_text",
					"text": "name of your environment"
				},
				"element": {
					"action_id": "environment",
					"type": "plain_text_input"
				}
			}
		],
		"close": {
			"type": "plain_text",
			"text": ":no_entry_sign: Cancel",
			"emoji": true
		},
		"submit": {
			"type": "plain_text",
			"text": "Submit Credentials"
		},
		"private_metadata": "auth",
		"clear_on_close": false,
		"notify_on_close": true
		}
