import http from "k6/http";

export const options = {
  discardResponseBodies: true,
  scenarios: {
    ramp_vus: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '15s', target: 5 },
        { duration: '15s', target: 10 },
        { duration: '15s', target: 20 },
        { duration: '15s', target: 40 },
        { duration: '15s', target: 50 },
        { duration: '5m', target: 50 },

      ],
      gracefulRampDown: '0s',
    },
  },
};

export default function () {

  const response = http.get('http://localhost:5000/raca/details?raca_id=abys');
}