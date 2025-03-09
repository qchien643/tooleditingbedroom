import axios from 'axios';

// flag sending data from chatbot : "message"
// flag sending data from user : "flowchart"


const sendToBackendDirec = async (data , url) => {
    try {
      const response = await axios.post(
        url,
        data,
        {
          withCredentials: true,
          headers: {
            "Content-Type": "application/json",
          },
        })
      
      return response.data; // Chỉ cần trả về response.data
    } catch (error) {
      console.error('Error sending data to the backend:', error);
      return 'Sorry, an error occurred.';
    }
  }

export default function sendDataBackend({data  , flag  , url="http://127.0.0.1:5000/api/chat" }){
    let data_extracted = {
        flag : flag ,
        data : data
    }
    // res = sendToBackendDirec(data_extracted , url);
    let res = {
        "status" : "success",
        "flag"   : flag ,
        "data" : {
            "chatbot" : "test ok",
            "human"   : "test ok"
        }
    }
    return res
}

// export default function sendDataBackend({ data, flag, url = "http://127.0.0.1:5000/api/chat" }) {
//     return new Promise((resolve) => {
//         setTimeout(() => {
//             let res = {
//                 "status": "success",
//                 "flag": flag,
//                 "data": {
//                     "chatbot": "test ok",
//                     "human": "test ok"
//                 }
//             };
//             resolve(res);
//         }, 2000); // Đợi 2 giây (2000ms)
//     });
// }
