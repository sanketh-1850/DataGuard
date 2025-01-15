import masking

def main():
    inp = '''We are thrilled to announce that Prime Analytics Pvt. Ltd. has successfully acquired VisionAI Systems, a leader in image recognition technology.

The acquisition, valued at ₹6,25,00,000, was led by Mr. Rahul Khanna, our Head of Corporate Finance. For questions regarding this acquisition, please contact him at rahul.khanna@primeanalytics.com or call +91-9123456789.

Transition plans for this integration will be shared by Ms. Neeta Deshmukh, VP of Operations, on January 30, 2025. She can be reached at neeta.deshmukh@primeanalytics.com or +91-9811223344.

This move marks a significant milestone in expanding our capabilities in AI-powered analytics.'''

    inp = masking.mask_using_regex(inp)

    inp = masking.mask_using_NER(inp)

    print(inp)


if __name__ == "__main__":
    main()