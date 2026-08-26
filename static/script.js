const chatMessages = document.getElementById("chat_messages");

const messageInput = document.getElementById("message_area");

const sendButton = document.getElementById("send");

const logoutButton = document.getElementById("logout-button");


sendButton.addEventListener("click", sendMessage);



messageInput.addEventListener("keydown", function (event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();
		
		console.log("Hello");
    }
});

logoutButton.addEventListener("click", async function () {

    await fetch("/logout", {
        method: "POST"
    });

    window.location.href = "/";
});


async function sendMessage()

{
	
	const message = messageInput.value.trim();
	
	if(!message)
	{
		
		return;
		
	}
	
	
	addMessage(message, "user");
	
	messageInput.value = "";
	
	sendButton.disabled = true;
	
	const thinkingMessage = addMessage("Thinking ...", "agent");
	
	try{
		
		const response = await fetch("/chat", {
					method:"POST",
					headers:{
						"Content-Type":"application/json"
						
					},
					body: JSON.stringify({
						message:message
						
					})
			
			
		});
		
		// If user session has expired or user is unauthorized
        if (response.status === 401) {

            window.location.href = "/";

            return;
        }

		
		if(!response.ok){
			
			throw new Error("Something Went wrong");
		}
		
		
		const data = await response.json();
		
		thinkingMessage.remove();
		
		addMessage(data.response, "agent");
		
	}
	
	catch(error)
	{
		thinkingMessage.remove();
		
		addMessage("Sorry, something went wrong. Please try again", "agent")
		
		Console.error(error)
	}
	
	finally{
		
		sendButton.disabled=false;
		
		messageInput.focus();
	}
	
	
	
}


// Function to display messages in the chat
function addMessage(text, sender) {

    const messageElement = document.createElement("div");

    messageElement.classList.add("message");
    messageElement.classList.add(sender);
	
	
    messageElement.textContent = text;

    chatMessages.appendChild(messageElement);

    
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return messageElement;
}


