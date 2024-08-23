class Converter:
    def __init__(self):
        self.numbers = ["०", "१", "२", "३", "४", "५", "६", "७", "८", "९"]

    def convert_to_hindi_numbers(self, english_num):
        """Converts English numbers to Hindi.

        Args:
        - english_num (str): The number in English.

        Returns:
        - str: The number in Hindi.
        """
        text = ""
        for char in english_num:
            if char.isdigit():
                text += self.numbers[int(char)]
            else:
                text += char
        return text


converter = Converter()
result = converter.convert_to_hindi_numbers("""४ ३.1४16 + ८१० ३.1४16 संसद के विशेष सत्र (Parliament Special Session) के बीच कल यानी, सोमवार, 18 सितंबर को प्रधानमंत्री नरेंद्र मोदी (PM Narendra Modi) की अध्यक्षता में हुई केंद्रीय कैबिनेट बैठक हुई जिसमें  महिला आरक्षण बिल (Women's Reservation Bill) मंजूरी दे दी गई है. 
    सूत्रों के हिसाब से यह खबर सामने आ रही है. 
    मोदी कैबिनेट की बैठक में लोकसभा और विधानसभाओं जैसी निर्वाचित संस्थाओं में 33 फीसदी महिला आरक्षण (Women Quota Bill 2023) पर मुहर लग गई है. 
    मीडिया रिपोर्ट्स के अनुसार, महिला आरक्षण बिल को आज यानी  मंगलवार को लोकसभा में नए संसद भवन (New Parliament Building) में पेश किया जाएगा.
    This line has less than three words.
    This line contains 90% non-Hindi characters and should be removed.
    12345 को १२३४५ में परिवर्तित किया जाना चाहिए""")
print(result)  # Output: "१२३४५"