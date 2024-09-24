export const sendMessageToApi = async (input, diseaseName = '') => {
  try {
    const response = await fetch('http://localhost:5001/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text: input, diseaseName: diseaseName })
    });

    if (!response.ok) {
      throw new Error('תקלה בשליחת ההודעה לשרת');
    }

    const data = await response.json();
    // console.log(data.response);
    return data;
  } catch (error) {
    throw error;
  }
};
