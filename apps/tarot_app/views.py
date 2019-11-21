from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

CARD_LIST = [
    {'name': 'The Fool', 'image': 'images/fool.jpg', 'description': 'Free spirit and unlimited potential.', 'categories': {
        'love': 'The Fool encourages you to have an open, curious mind and a sense of excitement. Throw caution to the wind and be ready to embrace the unknown, leaving behind any fear, worry     or anxiety about what may or may not happen. Today is about new experiences, personal growth, development, and adventure.', 
        'career': 'This is a time of great potential and opportunity for you right now. The world is your oyster, and anything can happen. Use your creative mind with a dash of spontaneity to     make the most of this magical time and bring forth your new ideas in powerful ways.', 
        'moody':'This is an excellent card to meditate on if you are struggling with dread, worry or self-doubt in your life. The Fool is your guide, as someone who is daring and            carefree. He is the embodiment of who you really are – your free spirit, your inner child, and your playful soul. Any time you experience fear, remember the essence of the Fool as he encourages you to acknowledge that fear and do it anyway! You never know what the future holds, but like the Fool, you must step into the unknown, trusting that the Universe will catch you and escort you along the way. Take a chance and see what happens.'}},
    {'name': 'The Magician', 'image': 'images/magician.jpg', 'description': 'Resourcefulness and power.', 'categories': {
        'love': 'a thing', 
        'career': 'The Magician brings you the tools, resources and energy you need to make your dreams come true. Seriously, everything you need right now is at your fingertips. You have the  spiritual (fire), physical (earth), mental (air) and emotional (water) resources to manifest your desires. And when you combine them with the energy of the spiritual and earthly realms, you will become a manifestation powerhouse! The key is to bring these tools together synergistically so that the impact of what you create is greater than the separate parts. Put your work into motion today. All you are missing today is discipline and momentum.',
        'home': 'a thing',
        'friendship': 'The Magician is symbolic of action and power in your life. Its positive connotations illustrate someone who is a smooth talker and good at all aspects of communication. This card suggests using your strong will power to move forward and take action. Use this superpower you have today to communicate with the people you surround yourself with. Bringing your ideas to the table and listening to others about theirs will help you form long lasting bonds.',
        'moody': 'Today is the perfect time to move forward on an idea that you recently conceived. The seed of potential has sprouted, and you are being called to take action and bring your intention to fruition. The skills, knowledge and capabilities you have gathered along your life path have led you to where you are now, and whether or not you know it, you are ready to turn your ideas into reality.' }},
    {'name': 'The High Priestess', 'image': 'images/high_priestess.jpg', 'description': 'Intuition and secret knowledge.', 'categories': {
        'love': 'The High Priestess signifies spiritual enlightenment, inner illumination, divine knowledge and wisdom. Today is a time of heightened intuitive ability and psychic insight. Follow your intuition as you may know more than others believe to do. This card may be a warning of concealed facts or influences that are, or will be important to you.', 
        'career': 'The High Priestess signifies spiritual enlightenment, inner illumination, divine knowledge and wisdom. Today, the undiscovered or repressed creative abilities you have are demanding to be expressed. Finding a spiritual guide will help you realize the full potential of your abilities. In order to get what you desire, you will need to overcome your fear of commitment.',
        'friendship': 'The High Priestess signifies spiritual enlightenment, inner illumination, divine knowledge and wisdom. This card is a signal to embrace more connection with others using your personal connection to your compassion and empathy. Feel, rather than think. Collaborate, rather than compete. Create, rather than destroy. Trust your energy even if the masculine energy around you may appear to be stronger. Be proud of your ability today to nurture, trust, sense and empathise instead of hiding it away.',
        'moody':'Your intuitive sense right now is providing you with useful information and is assisting you to become more in touch with your subconscious mind. Knowledge of how to fix these issues will not come through thinking and rationalising, but by tapping into and trusting your intuition, so allow yourself the time and space to meditate and attend to your inner voice. Look for areas in your life that may be out of balance or lacking ‘flow’ and ease.'}},
    {'name': 'The Empress', 'image': 'images/empress.jpg', 'description': 'Femininity, beauty, and nurture.', 'categories': {
        'love': 'The Empress signifies a strong connection with our femininity. Femininity translates in many ways – elegance, sensuality, fertility, creative expression, nurturing – and is necessary for creating balance in both men and women. The Empress calls on you to connect with your feminine energy. Create beauty in your life. Connect with your senses through taste, touch, sound, smell and sight. Draw on these senses to experience pleasure and deep fulfilment. /nWhen you are in tune with the energy of the Empress, you will naturally take on her mothering nature. Today, feel a strong urge to nurture and care for others, from a place of loving compassion and support. See it as a gift and an honour to tend to others, and in doing so you, too, receive benefit. In a more literal sense, you may step into the role of ‘mother’, perhaps as the mother of a newborn, caretaker of other people’s children, or spending more quality time with your kids. ', 
        'career': 'The Empress signifies a strong connection with our femininity. Femininity translates in many ways – elegance, sensuality, fertility, creative expression, nurturing – and is necessary for creating balance in both men and women. The Empress calls on you to connect with your feminine energy. Create beauty in your life. Connect with your senses through taste, touch, sound, smell and sight. Draw on these senses to experience pleasure and deep fulfilment. The Empress can also suggest pregnancy or birth. This may be an actual pregnancy or childbirth, or a metaphorical ‘birth’ of a new idea or project. Today, bring your creative ideas into being by nurturing them and supporting their growth. Allow those designs and their manifestation to flow through you, acting with compassion and love.',
        'home': 'The Empress signifies a strong connection with our femininity. Femininity translates in many ways – elegance, sensuality, fertility, creative expression, nurturing – and is necessary for creating balance in both men and women. The Empress calls on you to connect with your feminine energy. Create beauty in your life. Connect with your senses through taste, touch, sound, smell and sight. Draw on these senses to experience pleasure and deep fulfilment. The Empress in your reading today signifies abundance. You are surrounded by life’s pleasures and luxuries and have everything you need to live a comfortable lifestyle. You are in a period of growth, in which all you have dreamed of is now coming to fruition. Today, take a moment to reflect on the bounty that surrounds you and offer gratitude for all you have created so you can continue to build on this energy and create even more abundance in your life.',
        'friendship': 'The Empress signifies a strong connection with our femininity. Femininity translates in many ways – elegance, sensuality, fertility, creative expression, nurturing – and is necessary for creating balance in both men and women. The Empress calls on you to connect with your feminine energy. Create beauty in your life. Connect with your senses through taste, touch, sound, smell and sight. Draw on these senses to experience pleasure and deep fulfilment. /nToday, the Empress urges you to venture out. You have been inside, continuing the same routines. Invite a friend into nature today to ground your energy and be in flow with the earth. Take a trip to your favourite natural setting, be it a walk around your local park, beach, or lake, and sit for a couple of minutes or even hours to breathe in the energy that surrounds you while marvelling in the beauty of your surroundings. Share this often forgotten possible recess with someone you wish to connect with today! Allow the time and the space to enter a different frame of mind and receive the grounding spirit of nature into your heart and consciousness.',
        'moody':'Today, the Empress encourages you to make self-love and self-care a priority. Now is the time to bring your loving energy and focus to yourself, especially if you have been giving away your personal power by placing too much emphasis on another person’s emotional or material needs, thus neglecting your own. Book a dinner or a weekend, go for a walk on your own or start a creative project that’s just for you. It is essential that you fill your cup and care for yourself so you can then take care of others without resentment.'}},
    {'name': 'The Emperor', 'image': 'images/emperor.jpg', 'description': 'Authority and Structure', 'categories': {
        'love': 'As the father figure of the Tarot deck, the Emperor suggests that you are adopting this fatherly role (regardless of whether you are male or female), providing for your family, and protecting and defending your loved ones. You may be the breadwinner or the ‘rock’ for those who rely on your stability and security. Today, make sure you fill in this Emperor role. Assure the person most important in your life your pledge to assist them in their difficulties. Whatever they may be, your love deserves to know this.', 
        'career': 'The Emperor represents a powerful leader who demands respect and authority. Status, power and recognition are essential to you, and you are most comfortable in a leadership role where you can command and direct others. As a leader, you rule with a firm but fair hand. You have a clear vision of what you want to create, and you organise those around you to manifest your goal. Today, listen to the advice of others, but prefer to have the final say. Conflict doesn’t scare you, and you won’t hesitate to use your power to protect those you care about. And in return, those people will repay you with the loyalty and respect you deserve. Claim your authority as leader and influencer and don’t let others put you down. /nThere may be a moment where someone in a position of authority offers to help you. In any form, the more experienced hand that has come to help you may be more capable than yours. Protecting your loved ones is important, but those in a leadership position must know how to compromise. Beware the overly-dependant.',
        'home': 'As the father figure of the Tarot deck, the Emperor suggests that you are adopting this fatherly role (regardless of whether you are male or female), providing for your family, and protecting and defending your loved ones. You may be the breadwinner or the ‘rock’ for those who rely on your stability and security. Today, take a step to encourage support and happiness to those you share home with in your life.',
        'friendship': 'As the father figure of the Tarot deck, the Emperor suggests that you are adopting this fatherly role (regardless of whether you are male or female), providing for your friends, and protecting and defending your loved ones. You may be the ‘rock’ for those who rely on your stability and security.',
        'moody':'The Emperor reflects a system bound by rules and regulations. You create law and order by applying principles or guidelines to a specific situation. Today, create calm out of chaos by breaking down any problem into its parts and then mapping out the actions you need to take to resolve it. Be systematic, strategic and highly organised in your approach, and stick to your plan until the end.'}},
    {'name': 'The Hierophant', 'image': 'images/hierophant.jpg', 'description': 'Conformity, traditions, and institutions', 'categories': {
        'love': 'If you already have a loved one, consider their hand in marriage. /nIf you are already married, reflect on all aspects of your partner that made you fall in love in the first place. /nIf you dont have a significant other today, reflect on five aspects about yourself that you love and others would love about you as well.', 
        'career': 'If you have already mastered a particular field of study, today you may consider taking on the role of teacher and mentor to others. In this position, you honour and acknowledge your responsibility to share your knowledge in a structured way.'
        ,'home': 'Today the Hierophant may call you to honour family traditions or sacred rituals that sit neglected. You are being asked to commit to  practice in its most wholesome form – no customisation, no adaptation, no bending the rules. If you have been lacking ritual and tradition, create a regular practice such as daily meal with your family or saying "I love you." before leaving for the day. Consider exploring your family heritage.',
        'friendship': 'The Hierophant Tarot card often speaks to group membership or being part of an institution. You may enjoy a deep sense of comfort being surrounded by people who have similarities in beliefs and values. Finding them may be as significant as exploring a new hobby or club, or as simple as joining a gym or Coding Dojo community. This card is about identifying with others and a way of thinking that will prompt solid future friendships and further learning.',
        'moody':'If you are considering nonconformity today. Dont. The Hierophant‘s arrival suggests you should follow convention and stay within the bounds of a ‘tried and tested’ model. You are not yet willing to go out on a limb or offer any new and innovative ideas. So for the time being, you should adhere to the key principles and rules that you know will lead to a successful result. Remember, if the others around you are capable of being wrong, so are you.'}},
    {'name': 'The Lovers', 'image': 'images/lovers.jpg', 'description': 'Relationships and values alignment.', 'categories': {
        'love': 'Lucky you! This card is a great card. The lovers represents the deep connection between two souls. There is a person in your life who love and care about you more than anything else. When you are away from each other, you are both on eachothers mind. The Lovers is a card of open communication and raw honesty. Given that the man and woman are naked, they are both willing to be in their most vulnerable states and have learned to open their hearts to one another and share their truest feelings. They shape the container from which trust and confidence can emerge, and this makes for a powerful bond between the two. In this reading today, this card is a sign that by communicating openly and honestly with those you care about, you will create a harmonious and fulfilling relationship built on trust and respect.', 
        'career': 'Today, the Lovers card encourages you to unify dual forces. You can bring together two parts that are seemingly in opposition to one another and create something that is ‘whole’, unified and harmonious. In every choice, there is an equal amount of advantage and disadvantage, opportunity and challenge, positive and negative. When you accept these dualities, you build the unity from which love flows. Take two contradicting aspects of your career today and bring the best of each part together, porque no los dos?',
        'home': 'Today, there is an approaching conflict that will test your values. In order to progress, you are going to have to make a decision between supporting a loved one or discouraging them. The choice will shape you and your priorities.',
        'friendship': 'In its purest form, the Lovers card represents conscious connections and meaningful relationships. The arrival of this card in a Tarot reading shows that you have a beautiful, soul-honouring connection with a loved one. While the Lovers card typically refers to a romantic tie, it can also represent a close friendship or family relationship where love, respect and compassion flow.',
        'moody':'At its heart, the Lovers is about choice. Today, you have the choice about who you want to be in this lifetime, how you connect with others and on what level, and about what you will and won’t stand for. To make good choices, you need to be clear about your personal beliefs and values – and stay true to them. Not all decisions will be easy either. The Lovers card is often a sign that you are facing a moral dilemma and must consider all consequences before acting. Your values system is being challenged, and you are being called to take the higher path, even if it is difficult. Do not carry out a decision based on fear or worry or guilt or shame. Now, more than ever, you must choose love – love for yourself, love for others and love for the Universe. Choose the best version of yourself. For love.'}},
    {'name': 'The Chariot', 'image': 'images/chariot.jpg', 'description': 'Control and determination', 'categories': {
        'love': 'In a very literal sense, the Chariot can represent travel, especially driving or taking a road trip. Take your loved one to see and experience something brand new. You may even be considering renting an RV. Give yourself a refresher and a sense of inspiration. Life is for the living!', 
        'career': 'The Chariot is a card of willpower, determination and strength. When the Chariot appears in a Tarot reading, take it as a sign of encouragement. You have set your objectives and are now channelling your inner power with a fierce dedication to bring them to fruition. When you apply discipline, commitment and willpower to achieve your goals, you will succeed. /nIf you are curious about whether you have what it takes to achieve your aim or complete an important project, the Chariot is a sign you will be successful so long as you keep your focus and remain confident in your abilities. You need to use your willpower and self-discipline to concentrate on the task at hand. You can’t cut corners or take the easy route, or you will fail. Instead, see this endeavour as a test of your strength and conviction, and recognise that victory is within reach, but it’s up to you to follow through.',
        'friendship': 'The Chariot calls you to assert yourself and be courageous. Today be bold in expressing your desires and laying down your boundaries; otherwise, you will not get your way. You need to have faith in yourself and know fundamentally who you are and what you stand for. Your friends and loved ones who care about you will be able to understand you better.',
        'moody':'Now isn’t the time to be passive in the hope that things will work out in your favour. Today, take focused action and stick to the course, no matter what challenges may come your way – because, believe me, there will be challenges. You may be pulled in opposite directions and find your strength and conviction tested. Others may try to block you, distract you, or drag down the pursuit of your goal. But the Chariot is an invitation to draw upon your willpower and home in on what’s essential to you, so you can push past the obstacles in your way.'}},
    {'name': 'Strength', 'image': 'images/strength.jpg', 'description': 'Mental strength, influence, and compassion.', 'categories': {
        'love': 'Today, the Strength card urges you to ‘tame’ your animal instincts, gut reactions, and raw emotions, and channel these initial responses constructively. It’s normal for feelings such as anger, rage, sadness, guilt or shame to arise in certain situations. However, it’s what you do with these emotions that makes all the difference. Now is a time when you need to be conscious of your instinctual urges and bring them into balance with the greater good. This is no time to act out in rage or hatred. Approach your situation from a place of forgiveness, love and compassion.', 
        'career': 'When the Strength Tarot card appears in a reading, you are fuelled by your inner strength, personal power, strong will and determination. Today, you do not rule by trying to control others; you quietly influence and persuade. Others may underestimate your power because it is so ‘invisible’ – but you should see that as an advantage. You can control a situation without excessive, outward force. No one knows it’s you calling the shots.',
        'friendship': 'Your strength gives you the confidence to overcome any growing fears, challenges or doubts. Feel the fear and do it anyway! If you have been going through a rough time and are burnt out or stressed, the Strength card encourages you to find the power within yourself to persevere. You have got what it takes to see this situation through to its eventual end. You’re a loyal friend and a solid supporter, willing to step up and be present when others are in need, and you might also feel compelled to hold space for someone who needs your strength and support.',
        'moody':'Today, the Strength card speaks to the inner strength and the human spirits ability to overcome any obstacle. Strength is about knowing you can endure life’s obstacles. You have great stamina and persistence, balanced with underlying patience and inner calm. You are committed to what you need to do, and you go about it in a way that shows your composure and maturity.'}},
    {'name': 'The Hermit', 'image': 'images/hermit.jpg', 'description': 'Being alone and inner guidance.', 'categories': {
        'career': 'The Hermit often appears when you are at a pivotal point in your life and considering a new direction. Through meditation, contemplation, and self-examination, you may begin to re-evaluate your personal goals and change your overall course. You will look at your life with a deeper, more firm understanding and a few of your priorities will change as a result.',
        'home': 'The Hermit also represents the desire to turn away from a consumerist or materialistic society to focus on your inner world. Have you ever seen (or read) Into the Wild? After graduating from university, top student and athlete Christopher McCandless abandons his possessions, gives his entire $24,000 savings account to charity and hitchhikes to Alaska to live in the wilderness alone. Whilst his story has a tragic ending, his journey into the wild was like that of the Hermit, who seeks answers within and knows they will come only with quiet and solitude.',
        'friendship': 'The Hermit invites you to retreat into your private world and experience a deep sense of seclusion and introspection. You know that you need to take this journey alone or with a small, intimate group of like minded people. When you allow yourself to tune in to your inner, guiding light, you will hear the answers you need and grow wise beyond your years. Find your light, shine it on your soul and create your unique path. You will see what lies ahead of you – not miles upon miles, but enough to know where to step next. From there, take one step at a time.',
        'moody':'The Hermit shows that today you are taking a break from everyday life to draw your energy and attention inward and find the answers you seek, deep within your soul. You realise that your most profound sense of truth and knowledge is within yourself and not in the distractions of the outside world. You leave behind the mundane to set off on a journey of self-discovery, led only by your inner wisdom and guiding light. Now is the perfect time to go on a weekend retreat or sacred pilgrimage, anything in which you can contemplate your motivations, personal values and principles, and get closer to your authentic self.'}},
    {'name': 'Wheel of Fortune', 'image': 'images/wheel_of_fortune.jpg', 'description': 'Great luck and destiny', 'categories': {
        'love': 'The Wheel of Fortune is also known as the wheel of karma and reminds you that ‘what goes around comes around.’ Be a kind and loving person to others, and they’ll be kind and loving to you. Be nasty and mean, and you will get nasty and mean turning back your way. So, if you want happiness and abundance, make sure you’re sending out that positive juju in kind. What you send out into the Universe will come back your way.', 
        'career': 'At work, if you are someone who likes to have control and stability, then the Wheel of Fortune may come as a shock to the system. This Tarot card suggests that factors outside your control are influencing your situation. Today, it may seem as though the Universe is dishing up whatever it pleases; it is unpredictable and unnerving. This is one of the challenging aspects of the Wheel of Fortune since no matter which way the Wheel turns, it is impossible to try to change it. You need to accept what is happening and adapt. Go with the flow!',
        'home': 'The Wheel of Fortune card asks you to be optimistic and have faith that the Universe will take care of your situation in the best way possible. Meditation and visualisation can reinforce your intention to bring increased abundance, good fortune and prosperity to you and your home. Your life is about to turn in more positive directions if you are willing to grow and expand. Keep your mind open to all kinds of synchronicities and signs from the Universe. The magic of fate and destiny is behind you, and miracles are happening.',
        'moody':'The Wheel of Fortune reminds you that the wheel is always turning and life is in a state of constant change. If you’re going through a difficult time rest assured that it will get better from here. Good luck and good fortune will make their return in time. Similarly, if things are going well, know this, too, will change and life may return to ‘normal’ soon. This cycle shows why it is so important to cherish the blissful moments in your life and make the most of them while they are within reach – because in a flash they could be gone.'}},
    {'name': 'Justice', 'image': 'images/justice.jpg', 'description': 'Fairness and law.', 'categories': {
        'love': 'Justice is a very good card to find in your spread if you have acted with kindness and fairness towards other and, especially, if you have been a victim. It is a significant indicator of a positive resolution, although how and what sort will depend on your own experiences. If you have been unfair, abusive, or otherwise shady and immoral in your dealings, though, pay heed. For the unjust, this card is, at best, a dire warning to change your ways before retribution falls upon you, and, at worst, a simple statement that it is already too late. In neutral cases, it may simply be telling you to seek out balance in your life.', 
        'career': 'At its core, Justice is about the search for truth. As you explore your truth, you will discover that things are not as clear-cut as you had thought. Be prepared to dip into the murky waters and explore what truth means to you. Be consciously aware of what you believe to be true and what you believe to be fair and ethical. It may not be as clear-cut as you think, so prepare to challenge yourself and to explore new territories of your belief system.',
        'home': 'Treat others how you would like to be treated. Also treat others upon how they treat your loved ones. Recently, if one of your loved ones have been treated wrongly, make sure you seek justice and give them a bit of their own medicine. You may be used to choosing the higher road and to ignore toxic people. Today the justice card asks you to call them a bitch. ',
        'friendship': 'The Justice card often appears when you need to make an important choice with the potential for long-term repercussions. Be aware of the impact your decisions will have on your well-being and the well-being of others. Choose consciously by connecting with your inner guidance system (your intuition) and asking for the answer that is most in alignment with the highest good of all. Be ready to stand by your decisions as you will be held to account for the choices you make. You need to ask yourself, “Do I stand by my decisions and accept the consequences of my actions?” If you cannot, then dig deeper, plunging into the shadows of what is right and wrong, until you find the place where you can stand in integrity and strength.',
        'moody':'The Justice card represents justice, fairness, truth and the law. You are being called to account for your actions and will be judged accordingly. If you have acted in alignment with your Higher Self and for the greater good of others, you have nothing to worry about. However, if you haven’t, you will be called out and made to own up to your actions. If this has you shaking in your boots, know that the Justice card isn’t as black and white as you may think. A level of compassion and understanding accompany Justice, and although you may have done something you regret, this card suggests that you will be treated fairly and without bias. Be ready to take responsibility for your actions and stand accountable for the ensuing consequences.'}},
    {'name': 'The Hanged Man', 'image': 'images/hanged_man.jpg', 'description': 'New perspectives', 'categories': {
        'love': 'If there is something in your love life that feels rushed, this may suggest that it is going to pause. Today you may want to retreat and consider the future of the relationship. If you’re single, the Hanged Man signifies choices. Plenty of options will surface, and you don’t want to waste this chance by not making a choice.', 
        'career': 'When the Hanged Man appears in a Tarot reading, your projects and activities may be coming to an unexpected and abrupt halt. Don’t keep pushing forward, hoping that more force will drive you to where you want to go. Instead, surrender to the opportunity to pause and view it as your chance to reassess and re-evaluate where you are on your path. Something new is emerging, and you won’t be able to see it unless you allow the time and space for it to come through.',
        'home': 'The Hanged Man is your invitation to welcome these ‘pauses’ with open arms and surrender to the ‘what is’ – even if it is different from what you expected. Take time away from your routine to connect with a new way of thinking and seeing. Spend more time with family today and focus on their perspectives on life. Take a short break from your focus to see a bigger picture.',
        'friendship': 'The Hanged Man can sometimes reflect that you are feeling stuck or restricted in your life. What is holding you in this ‘stuck’ position? What is preventing you from moving forward? On one level, the Hanged Man is asking you to surrender and let go. Instead of investing in specific outcomes or resisting your current circumstances, accept them and allow yourself to flow with life. On another level, you are being called to change your perspective and shift your energy and may find that separating yourself from your everyday life is helpful, whether it’s going to that party and being social with new friends, going on a retreat or taking up that new class or hobby you have been considering. Change up your routine so you can start to shift your energy and flow more freely again.',
        'moody':'The Hanged Man reminds you that sometimes you have to put everything on hold before you can take the next step, or the Universe will do it on your behalf (and it may not always be at the most convenient time!). You may have heard the saying, ‘What got you here won’t get you there’, and that indeed is at play in this card. The Hanged Man calls you to release the old mental models and behavioural patterns that no longer serve you so you can see your world from a new perspective and embrace new opportunities that would have otherwise been hidden from you if you didn’t hit the brakes.'}},
    {'name': 'Death', 'image': 'images/death.jpg', 'description': 'Endings and transition.', 'categories': {
        'love': 'Death shows a time of significant transformation, change and transition. Today, you need to transform yourself and clear away the old to bring in the new. Any change should be welcomed as a positive, cleansing, transformational force in your life. The death and clearing away of limiting factors can open the door to a broader, more satisfying experience of life. This will attract others curiosity and interest in you.', 
        'career': 'The Death card has elements of a sudden and unexpected change. Death happens to everyone, no matter who you are, how much money you have, where you live, or what colour your skin is; it is the same with a significant change. So, the Death card can be a sign you may feel as though you are caught in the path of sweeping change and cannot escape its effects. Although the upheaval may seem unwanted and painful, this massive change could bring with it a series of unexpected surprises that create new opportunities and advantages for you. Every ending, has a new beginning.',
        'home': 'a thing',
        'friendship': 'a thing',
        'moody':'The Death card is probably the most feared and misunderstood of all the cards in the Tarot deck. Just mention the card’s name and most people freak out, worried they will suddenly keel over and die as soon as this card appears. Relax! The Death card can be one of the most positive cards in the deck. You must close one door to open another. You need to put the past behind you and part ways, ready to embrace new opportunities and possibilities. It may be difficult to let go of the past, but you will soon see its importance and the promise of renewal and transformation. If you resist these necessary endings, you may experience pain, both emotionally and physically, but if you exercise your imagination and visualise a new possibility, you allow more constructive patterns to emerge.'}},
    {'name': 'Temperance', 'image': 'images/temperance.jpg', 'description': 'we live in a society', 'categories': {
        'love': 'a thing', 
        'career': 'another thing',
        'home': 'a thing',
        'friendship': 'a thing',
        'moody':''}},
    {'name': 'The Devil', 'image': 'images/devil.jpg', 'description': 'we live in a society', 'categories': {
        'love': 'a thing', 
        'career': 'another thing',
        'home': 'a thing',
        'friendship': 'a thing',
        'moody':''}},
    {'name': 'The Tower', 'image': 'images/tower.jpg', 'description': 'we live in a society', 'categories': {
        'love': 'a thing', 
        'career': 'another thing',
        'home': 'a thing',
        'friendship': 'a thing',
        'moody':''}},
    {'name': 'The Star', 'image': 'images/star.jpg', 'description': 'we live in a society', 'categories': {
        'love': 'a thing', 
        'career': 'another thing',
        'home': 'a thing',
        'friendship': 'a thing',
        'moody':''}},
    {'name': 'The Moon', 'image': 'images/moon.jpg', 'description': 'we live in a society', 'categories': {
        'love': 'a thing', 
        'career': 'another thing',
        'home': 'a thing',
        'friendship': 'a thing',
        'moody':''}},
    {'name': 'The Sun', 'image': 'images/sun.jpg', 'description': 'we live in a society', 'categories': {
        'love': 'a thing', 
        'career': 'another thing',
        'home': 'a thing',
        'friendship': 'a thing',
        'moody':''}},
    {'name': 'Judgement', 'image': 'images/judgement.jpg', 'description': 'we live in a society', 'categories': {
        'love': 'a thing', 
        'career': 'another thing',
        'home': 'a thing',
        'friendship': 'a thing',
        'moody':''}},
    {'name': 'The World', 'image': 'images/world.jpg', 'description': 'we live in a society', 'categories': {
        'love': 'a thing', 
        'career': 'another thing',
        'home': 'a thing',
        'friendship': 'a thing',
        'moody':''}},


    {'name': 'Ace of Wands', 'image': 'images/wands_ace.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Two of Wands', 'image': 'images/wands_twp.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Three of Wands', 'image': 'images/wands_three.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Four of Wands', 'image': 'images/wands_four.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Five of Wands', 'image': 'images/wands_five.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Six of Wands', 'image': 'images/wands_six.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Seven of Wands', 'image': 'images/wands_seven.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Eight of Wands', 'image': 'images/wands_eight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Nine of Wands', 'image': 'images/wands_nine.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Ten of Wands', 'image': 'images/wands_ten.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Page of Wands', 'image': 'images/wands_page.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Knight of Wands', 'image': 'images/wands_knight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Queen of Wands', 'image': 'images/wands_queen.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'King of Wands', 'image': 'images/wands_king.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},

    {'name': 'Ace of Swords', 'image': 'images/swords_ace.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Two of Swords', 'image': 'images/swords_twp.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Three of Swords', 'image': 'images/swords_three.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Four of Swords', 'image': 'images/swords_four.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Five of Swords', 'image': 'images/swords_five.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Six of Swords', 'image': 'images/swords_six.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Seven of Swords', 'image': 'images/swords_seven.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Eight of Swords', 'image': 'images/swords_eight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Nine of Swords', 'image': 'images/swords_nine.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Ten of Swords', 'image': 'images/swords_ten.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Page of Swords', 'image': 'images/swords_page.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Knight of Swords', 'image': 'images/swords_knight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Queen of Swords', 'image': 'images/swords_queen.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'King of Swords', 'image': 'images/swords_king.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},

    {'name': 'Ace of Cups', 'image': 'images/cups_ace.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Two of Cups', 'image': 'images/cups_twp.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Three of Cups', 'image': 'images/cups_three.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Four of Cups', 'image': 'images/cups_four.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Five of Cups', 'image': 'images/cups_five.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Six of Cups', 'image': 'images/cups_six.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Seven of Cups', 'image': 'images/cups_seven.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Eight of Cups', 'image': 'images/cups_eight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Nine of Cups', 'image': 'images/cups_nine.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Ten of Cups', 'image': 'images/cups_ten.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Page of Cups', 'image': 'images/cups_page.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Knight of Cups', 'image': 'images/cups_knight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Queen of Cups', 'image': 'images/cups_queen.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'King of Cups', 'image': 'images/cups_king.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},

    {'name': 'Ace of Pentacles', 'image': 'images/pentacles_ace.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Two of Pentacles', 'image': 'images/pentacles_twp.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Three of Pentacles', 'image': 'images/pentacles_three.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Four of Pentacles', 'image': 'images/pentacles_four.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Five of Pentacles', 'image': 'images/pentacles_five.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Six of Pentacles', 'image': 'images/pentacles_six.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Seven of Pentacles', 'image': 'images/pentacles_seven.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Eight of Pentacles', 'image': 'images/pentacles_eight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Nine of Pentacles', 'image': 'images/pentacles_nine.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Ten of Pentacles', 'image': 'images/pentacles_ten.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Page of Pentacles', 'image': 'images/pentacles_page.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Knight of Pentacles', 'image': 'images/pentacles_knight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Queen of Pentacles', 'image': 'images/pentacles_queen.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'King of Pentacles', 'image': 'images/pentacles_king.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
]




def index(request):
    context = {
        "cards" : CARD_LIST
    }
    return render(request, "tarot_app/login.html",context)


def register(request):
    if request.method == 'POST':
        errors = User.objects.registration_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            new_user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                city_state= request.POST["city_state"],
                email=request.POST['email'],
                password=pw_hash
            )
            request.session['user_id'] = new_user.id
            request.session['first_name'] = new_user.first_name
            request.session['email'] = new_user.email
            return render(request, 'tarot.html')


def tarot(request):
    if not 'user_id' in request.session:
        messages.error(request, "Please log in!")
        return redirect ('/')
    return render(request,'tarot_app/tarot.html')


def login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
        except:
            messages.error(request, "Either your email or password was input incorrectly.")
            return redirect('/')
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()): 
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            return redirect('/tarot')
        else:
            messages.error(
                request, "Either your email or password was input incorrectly.")
            return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')


def tarot_question(request):
    return render(request, 'tarot_app/questionaire.html')

def tarot_question_mood(request):
    if request.method=="POST":
        # do stuff
        return redirect("/tarot/questionaire/mood_ask")

def tarot_question_mood_ask(request):
    if request.method=="POST":
        #morestuff
        return redirect("/")