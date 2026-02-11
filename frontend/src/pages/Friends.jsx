import { useEffect, useState } from "react";
import api from "../api/axios";

export default function Friends() {
  const [friends, setFriends] = useState([]);

  useEffect(() => {
    api.get("friends/list/").then((res) => {
      setFriends(res.data);
    });
  }, []);

  return (
    <div>
      {friends.map((f) => (
        <div key={f.uid}>{f.username}</div>
      ))}
    </div>
  );
}
