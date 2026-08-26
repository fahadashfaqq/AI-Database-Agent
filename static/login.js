const loginForm = document.getElementById("login-form");

const emailInput = document.getElementById("login_email");

const errorMessage = document.getElementById("error-message");

loginForm.addEventListener("submit", async function(event)
{
    event.preventDefault();

    const email = emailInput.value.trim();

    if(!email)
    {
        errorMessage.textContent = "Please enter your email.";
        return;

    }

    try{

        const response =await fetch("/login",{

            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                email:email
            })


        });

        const data =await response.json();

        if(response.ok)
        {
            window.location.href= "/";
        }
        else{
            errorMessage.textContent=data.detail || "Access denied.";
        }

    }

    catch(error)
    {
        console.error("Login error:", error);
        errorMessage.textContent = "Something went wrong. pelease try again";
    }

});