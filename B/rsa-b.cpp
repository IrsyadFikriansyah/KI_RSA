#include <cstdlib>
#include <iostream>
#include <vector>
using namespace std;

class Key {
   private:
    pair<int, int> publicKey;
    pair<int, int> privateKey;

    void setPublicKey(int e, int n) { publicKey = make_pair(e, n); }

    void setPrivateKey(int d, int n) { privateKey = make_pair(d, n); }

   public:
    Key() = default;

    // Constructor to initialize keys securely
    Key(int e, int n, int d, int m) {
        setPublicKey(e, n);
        setPrivateKey(d, m);
    }

    pair<int, int> getPublicKey() { return publicKey; }

    pair<int, int> getPrivateKey() { return privateKey; }

    int gcd(int a, int h) {
        int temp;
        while (1) {
            temp = a % h;
            if (temp == 0) return h;
            a = h;
            h = temp;
        }
    }

    int randNum(int n) { return rand() % n; }

    bool isPrime(int n) {
        if (n <= 1) return false;
        for (int i = 2; i <= sqrt(n); i++)
            if (n % i == 0) return false;
        return true;
    }

    int modInverse(int a, int m) {
        int m0 = m;
        int y = 0, x = 1;

        // If m is 1, the modular inverse is not defined
        if (m == 1) {
            return 0;
        }

        // Applying the extended Euclidean algorithm
        while (a > 1) {
            int q = a / m;
            int temp = m;

            m = a % m;
            a = temp;
            temp = y;

            y = x - q * y;
            x = temp;
        }

        // If the modular inverse is negative, make it positive
        if (x < 0) {
            x += m0;
        }

        return x;
    }

    void generateKey() {
        vector<int> prime;

        for (int i = 0; i < 100; i++) {
            if (isPrime(i)) prime.push_back(i);
        }

        // take 2 random prime numbers
        int p = prime[randNum(prime.size())];
        int q = prime[randNum(prime.size())];

        // if q is the same as p
        while (p == q) q = prime[randNum(prime.size())];

        printf("p : %d\nq : %d\n", p, q);

        int n = p * q;
        int phi = (p - 1) * (q - 1);

        vector<bool> selected(prime.size(), false);
        int e = randNum(phi);
        while (1) {
            if (gcd(e, phi) == 1)
                break;
            else
                e = (e + 1) % phi <= 1 ? 2 : (e + 1) % phi;
        }

        // Calculate the private exponent (d) such that (d * e) % phi = 1
        int d = modInverse(e, phi);

        // Set the keys directly in the current object
        setPublicKey(e, n);
        setPrivateKey(d, n);
    }
};

int main() {
    // Seed for random number generation
    srand(static_cast<unsigned>(time(0)));

    Key myKey;

    myKey.generateKey();

    // Retrieve and display the public key
    FILE *fp1 = fopen("../A/.key/publicKey-b.txt","w");
    pair<int, int> publicKey = myKey.getPublicKey();
    cout << "Public Key (e, n): (" << publicKey.first << ", " << publicKey.second << ")\n";
    fprintf(fp1,"%d\n%d", publicKey.first, publicKey.second);


    // Retrieve and display the private key
    FILE *fp2 = fopen(".key/privateKey-b.txt","w");
    pair<int, int> privateKey = myKey.getPrivateKey();
    cout << "Private Key (d, n): (" << privateKey.first << ", " << privateKey.second << ")\n";
    fprintf(fp2,"%d\n%d", privateKey.first, privateKey.second);


    fclose(fp1);
    fclose(fp2);

    return 0;
}