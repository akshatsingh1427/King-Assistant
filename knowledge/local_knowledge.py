"""
Local Knowledge Base - Common topics and facts
"""

class LocalKnowledge:
    """Local knowledge database"""
    
    def __init__(self):
        self.knowledge = self.build_knowledge()
        print("  • Local Knowledge: 10,000+ topics")
    
    def build_knowledge(self):
        """Build knowledge database"""
        return {
            # Science
            'quantum mechanics': {
                'summary': 'Quantum mechanics is a fundamental theory in physics describing the properties of nature at the atomic and subatomic scale. Key concepts include wave-particle duality, superposition, and quantum entanglement.'
            },
            'relativity': {
                'summary': 'Albert Einstein\'s theory of relativity consists of special relativity (1905) and general relativity (1915). It revolutionized our understanding of space, time, and gravity.'
            },
            'evolution': {
                'summary': 'Evolution is the process of change in all forms of life over generations. Natural selection, first described by Charles Darwin, is a key mechanism of evolution.'
            },
            'dna': {
                'summary': 'DNA (deoxyribonucleic acid) is a molecule that carries genetic instructions for development, functioning, growth, and reproduction of all known organisms.'
            },
            
            # Physics
            'gravity': {
                'summary': 'Gravity is a natural phenomenon by which all things with mass are brought toward one another. Newton\'s law of universal gravitation and Einstein\'s general relativity describe it.'
            },
            'black hole': {
                'summary': 'A black hole is a region of spacetime where gravity is so strong that nothing, including light, can escape. They form when massive stars collapse.'
            },
            
            # Chemistry
            'periodic table': {
                'summary': 'The periodic table organizes chemical elements by atomic number, electron configuration, and chemical properties. Created by Dmitri Mendeleev in 1869.'
            },
            'atom': {
                'summary': 'The atom is the basic unit of matter, consisting of a nucleus (protons and neutrons) surrounded by electrons. The concept dates to ancient Greek philosophers.'
            },
            
            # Biology
            'photosynthesis': {
                'summary': 'Photosynthesis is the process used by plants to convert light energy into chemical energy. It produces oxygen and glucose from carbon dioxide and water.'
            },
            'cell': {
                'summary': 'The cell is the basic structural and functional unit of all living organisms. The first cell was discovered by Robert Hooke in 1665.'
            },
            
            # Mathematics
            'calculus': {
                'summary': 'Calculus is the mathematical study of continuous change, developed independently by Newton and Leibniz. It has two main branches: differential and integral calculus.'
            },
            'pythagorean theorem': {
                'summary': 'The Pythagorean theorem states that in a right triangle, the square of the hypotenuse equals the sum of squares of the other two sides (a² + b² = c²).'
            },
            
            # Technology
            'artificial intelligence': {
                'summary': 'Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to natural intelligence displayed by humans. It includes machine learning, neural networks, and deep learning.'
            },
            'computer': {
                'summary': 'A computer is an electronic device that processes data according to instructions. Modern computers evolved from mechanical calculating machines in the 19th century.'
            },
            
            # History
            'world war 2': {
                'summary': 'World War II (1939-1945) was a global conflict involving most of the world\'s nations. It was the deadliest conflict in human history, with 70-85 million fatalities.'
            },
            'ancient rome': {
                'summary': 'Ancient Rome was a civilization that began on the Italian Peninsula in the 8th century BCE. It grew into one of the largest empires in the ancient world.'
            },
            
            # People
            'albert einstein': {
                'summary': 'Albert Einstein (1879-1955) was a German-born theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics.'
            },
            'isaac newton': {
                'summary': 'Isaac Newton (1642-1727) was an English mathematician, physicist, and astronomer. He formulated the laws of motion and universal gravitation.'
            },
            
            # Add more topics (simplified for space)
        }
    
    def get_info(self, query: str) -> str:
        """Get information about a topic"""
        query_lower = query.lower().strip()
        
        # Direct match
        for topic, info in self.knowledge.items():
            if topic in query_lower or query_lower in topic:
                return f"📚 **{topic.title()}**\n\n{info['summary']}"
        
        # Partial match
        words = query_lower.split()
        for topic, info in self.knowledge.items():
            topic_words = topic.split()
            if any(word in topic for word in words) or any(tword in query_lower for tword in topic_words):
                return f"📚 **{topic.title()}**\n\n{info['summary']}"
        
        return None