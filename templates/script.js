const btnSubmit = document.getElementById("submit-search-re");
const newEmail = document.getElementById("new-email");
const emailInput = document.querySelector("#email");
const requirementInput = document.querySelector("#requirement");
const sumOutput = document.querySelector(".summary");
const replyOutput = document.querySelector(".reply");
  
// function allowSelfSignedHttps(allowed) {
//   if (allowed && typeof window !== 'undefined' && window.process && window.process.env.NODE_TLS_REJECT_UNAUTHORIZED) {
//     window.process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
//   }
// }
// allowSelfSignedHttps(true);

const handleChat = async () => {
  try {
    emailMessage = emailInput.value.replace(/["'`]/g, "").replace(/\s+/g, ' ').trim();
    requireMessage = requirementInput.value.trim();
    const requestBody = `{
      "email": "${emailMessage}",
      "additional_context": "${requireMessage}"}`;

    const requestOptions = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer wWgs4sjQ4DbkvKP4uj3sPs2UDnCymeaG',
          'azureml-model-deployment': 'email-endpoint-2'},
        body: requestBody,};
    const response = await fetch('http://localhost:3000/api/send-request', requestOptions);
    const result = await response.text();
    replyOutput.value += JSON.parse(result)['reply'];
    sumOutput.value += JSON.parse(result)['sum'];
    // sumOutput.value += `${emailMessage}`;
    // replyOutput.value += `${requireMessage}`;
  } catch (error) {
      console.error('Error:', error);
  }
};

const removeconent = () => {
  emailInput.value = "";
  requirementInput.value = "";
  replyOutput.value = "";
  sumOutput.value = "";
}

btnSubmit.addEventListener('click', handleChat );
newEmail.addEventListener('click', removeconent )