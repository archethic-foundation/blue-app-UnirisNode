# UnirisNode App for Ledger Blue & Ledger Nano S

This application help Uniris Node to sign and Decrypt messages using a private key stored on the ledger device.

Run `make load` to build and load the application onto the device. After
installing and running the application, you can run `make delete` to delete the app from the ledger device.

To test the application just execute this: `python client.py data_to_sign`
Example: python client.py 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824