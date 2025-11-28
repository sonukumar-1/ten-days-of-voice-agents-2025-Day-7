import { motion } from 'motion/react';
import {
  ArrowRight,
  Hamburger,
  Fire,
  Crown,
} from '@phosphor-icons/react/dist/ssr';
import { FlameButton } from '@/components/ui/flame-button';

interface WelcomeViewProps {
  onStart: () => void;
}

export function WelcomeView({ onStart }: WelcomeViewProps) {
  return (
    <div className="relative flex min-h-screen w-full flex-col overflow-hidden bg-[#F5EBDC] font-sans text-[#502314] selection:bg-[#E55F25]/30">
      {/* Dynamic Background Elements - Burger King Theme */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute top-[-20%] left-[-10%] h-[800px] w-[800px] animate-float rounded-full bg-gradient-to-br from-[#E55F25]/20 to-transparent blur-[120px]" />
        <div className="absolute right-[-10%] bottom-[-20%] h-[800px] w-[800px] animate-float-delayed rounded-full bg-gradient-to-tl from-[#D62300]/10 to-transparent blur-[100px]" />
      </div>

      {/* Floating Food Emojis */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden opacity-20">
        <div className="absolute top-[10%] left-[10%] text-6xl animate-float">🍔</div>
        <div className="absolute top-[20%] right-[15%] text-5xl animate-float-delayed">🍟</div>
        <div className="absolute bottom-[15%] left-[20%] text-7xl animate-float">🥤</div>
        <div className="absolute bottom-[25%] right-[10%] text-6xl animate-float-delayed">🧅</div>
        <div className="absolute top-[50%] left-[5%] text-4xl animate-float">👑</div>
        <div className="absolute top-[40%] right-[5%] text-5xl animate-float-delayed">🔥</div>
      </div>

      <div className="relative z-10 flex flex-grow flex-col items-center justify-center px-6 py-20 text-center">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
          className="mb-12"
        >
          {/* Badge */}
          <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-[#D62300]/30 bg-[#D62300]/10 px-5 py-2 shadow-sm backdrop-blur-xl">
            <Fire weight="fill" className="h-4 w-4 text-[#D62300]" />
            <span className="text-xs font-bold tracking-widest text-[#D62300] uppercase">
              Flame Grilled Since 1954
            </span>
          </div>

          <h1 className="mb-8 text-6xl font-extrabold tracking-tight text-[#502314] drop-shadow-sm md:text-8xl">
            Burger <br />
            <span className="animate-gradient bg-300% bg-gradient-to-r from-[#D62300] via-[#E55F25] to-[#D62300] bg-clip-text text-transparent">
              King
            </span>
          </h1>

          <p className="mx-auto mb-10 max-w-2xl text-lg leading-relaxed font-bold text-[#502314]/80 md:text-xl">
            Home of the Whopper.
            <br />
            <span className="font-extrabold text-[#D62300]">
              Have it your way.
            </span>
          </p>
        </motion.div>

        {/* Feature Cards - Glassmorphism */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.8 }}
          className="mb-16 grid w-full max-w-5xl grid-cols-1 gap-6 md:grid-cols-3"
        >
          {[
            {
              icon: Hamburger,
              title: 'Flame Grilled',
              desc: '100% flame grilled, cooked to perfection.',
              gradient: 'from-[#D62300]/20 to-[#502314]/10',
              iconColor: 'text-[#D62300]',
            },
            {
              icon: Crown,
              title: 'King Deals',
              desc: 'Royal flavors at unbeatable prices.',
              gradient: 'from-[#E55F25]/20 to-[#502314]/10',
              iconColor: 'text-[#E55F25]',
            },
            {
              icon: Fire,
              title: 'Freshly Prepared',
              desc: 'Fresh ingredients, prepared daily.',
              gradient: 'from-[#D62300]/20 to-[#502314]/10',
              iconColor: 'text-[#D62300]',
            },
          ].map((feature, idx) => (
            <motion.div
              key={idx}
              whileHover={{ y: -8 }}
              className="group relative flex flex-col items-center rounded-3xl border border-[#502314]/10 bg-white/40 p-8 shadow-lg backdrop-blur-md transition-all duration-300 hover:border-[#D62300]/30 hover:shadow-[#D62300]/20"
            >
              <div
                className={`absolute inset-0 rounded-3xl bg-gradient-to-b ${feature.gradient} opacity-0 transition-opacity duration-500 group-hover:opacity-100`}
              />

              <div className="relative z-10 mb-6 rounded-2xl bg-white/60 p-4 shadow-sm ring-1 ring-[#502314]/10">
                <feature.icon className={`h-8 w-8 ${feature.iconColor}`} />
              </div>
              <h3 className="relative z-10 mb-3 text-xl font-bold text-[#502314]">
                {feature.title}
              </h3>
              <p className="relative z-10 text-sm font-medium text-[#502314]/70">{feature.desc}</p>
            </motion.div>
          ))}
        </motion.div>

        {/* CTA Button - Burger King Red */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.4, duration: 0.5 }}
        >
          <FlameButton onClick={onStart} />
        </motion.div>
      </div>

      {/* Footer */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1, duration: 1 }}
        className="relative z-10 mt-auto mb-8 flex flex-col items-center gap-2"
      >
        <div className="h-px w-12 bg-gradient-to-r from-transparent via-[#502314]/20 to-transparent" />
        <span className="text-[10px] font-medium tracking-[0.2em] text-[#502314]/40 uppercase">
          Powered by LiveKit & Gemini
        </span>
      </motion.div>
    </div>
  );
}
