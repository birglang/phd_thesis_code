module.exports = {
  rpc: {
    host:"127.0.0.1",
    port:8545
  },
  networks: {
    development: {
      host: "127.0.0.1",
      port: 8545,
      network_id: "*" // Match any network id
    }
  }
};