import axios from 'axios';

// flag sending data from chatbot : "message"
// flag sending data from user : "flowchart"


export async function sendRefreshSignal(url="http://127.0.0.1:5000/api/refresh") {
  try {
    // Gửi request POST đến endpoint /refresh (bạn có thể đổi tuỳ ý)
    const response = await axios.post(url, {
      flag: 'refresh',
      status : "",
      data: ''
    });
    return response.data;
  } catch (error) {
    console.error('Error sending refresh signal:', error);
    throw error;
  }
}

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

export default function sendDataBackend({data  , flag  , status = "" , url="http://127.0.0.1:5000/api/chat" }){
    let data_extracted = {
        flag : flag ,
        status : status ,
        data : data
    }
    let res = sendToBackendDirec(data_extracted , url);
    // let res = {
    //     "status" : "success",
    //     "flag"   : flag ,
    //     "data" : {
    //         "chatbot" : "test ok",
    //         "human"   : "test ok"
    //     }
    // }
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
