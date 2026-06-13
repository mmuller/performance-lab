import http from "k6/http";
import { check } from "k6";

const baseUrl = (__ENV.BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

export const options = {
  vus: 5,
  duration: "30s",
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<500"],
  },
};

export default function () {
  const response = http.get(`${baseUrl}/work`);
  const body = response.json();

  check(response, {
    "status is 200": (res) => res.status === 200,
    "work is completed": () => body.status === "completed",
    "response includes request_id": () => Boolean(body.request_id),
  });
}
