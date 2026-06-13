import http from "k6/http";
import { check } from "k6";

const baseUrl = (__ENV.BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

export const options = {
  stages: [
    { duration: "10s", target: 5 },
    { duration: "20s", target: 5 },
    { duration: "20s", target: 20 },
    { duration: "20s", target: 20 },
    { duration: "10s", target: 0 },
  ],
  thresholds: {
    http_req_failed: ["rate<0.01"],
    checks: ["rate>0.99"],
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
