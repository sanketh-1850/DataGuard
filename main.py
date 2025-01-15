import masking

def main():
    inp = '''At Innovate Solutions Pvt. Ltd., we are committed to providing exceptional service while maintaining transparency with our stakeholders. As part of our growth strategy, we are pleased to announce the acquisition of TechSynergy LLC to expand our portfolio in AI-driven analytics.

    This acquisition involves an investment of ₹12,50,00,000, which has been secured through strategic funding from Global Ventures Capital, led by our CFO, Mr. Arjun Nair. For inquiries related to this acquisition, please contact Mr. Nair directly at arjun.nair@innovatesolutions.com or +91-9812345678.

    All teams involved in the transition will receive additional instructions from Ms. Pooja Singh, Head of Corporate Development, by January 20, 2025. Her contact details are pooja.singh@innovatesolutions.com and +91-9922334455.

    We are excited about this new chapter and believe it will enable us to better serve our clients and expand our market reach.'''

    inp = masking.mask_using_regex(inp)

    inp = masking.mask_using_NER(inp)

    print(inp)


if __name__ == "__main__":
    main()