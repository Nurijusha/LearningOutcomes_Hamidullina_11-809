import React from "react";
import {
  useParams,
  useNavigate
} from "react-router-dom";

function Activate() {
  let { uid, token } = useParams();
  const navigate = useNavigate();

  React.useEffect(() => {
    fetch("/api/users/activation/", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        uid, token
      })
    })
      .then((response) => {
        if (response.ok) {
          navigate(`/congratulation`)
        }
      })
  }, [])

  return (
    <div>
    </div>
  );
}

export default Activate;
